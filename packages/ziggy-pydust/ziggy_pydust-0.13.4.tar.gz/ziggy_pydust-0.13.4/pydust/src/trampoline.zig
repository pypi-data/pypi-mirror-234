// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//         http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/// Utilities for bouncing CPython calls into Zig functions and back again.
const std = @import("std");
const Type = std.builtin.Type;
const ffi = @import("ffi.zig");
const py = @import("pydust.zig");
const State = @import("discovery.zig").State;
const funcs = @import("functions.zig");
const pytypes = @import("pytypes.zig");
const PyError = @import("errors.zig").PyError;

/// Generate functions to convert comptime-known Zig types to/from py.PyObject.
pub fn Trampoline(comptime T: type) type {
    // Catch and handle comptime literals
    if (T == comptime_int) {
        return Trampoline(i64);
    }
    if (T == comptime_float) {
        return Trampoline(f64);
    }

    return struct {
        /// Recursively decref an object-like. No-op for non-objects.
        pub inline fn decref_objectlike(obj: T) void {
            if (isObjectLike()) {
                asObject(obj).decref();
                return;
            }
            switch (@typeInfo(T)) {
                .Struct => |s| {
                    inline for (s.fields) |f| {
                        Trampoline(f.type).decref_objectlike(@field(obj, f.name));
                    }
                },
                else => {},
            }
        }

        /// Wraps an object that already represents an existing Python object.
        /// In other words, Zig primitive types are not supported.
        pub inline fn asObject(obj: T) py.PyObject {
            switch (@typeInfo(T)) {
                .Pointer => |p| {
                    // The object is an ffi.PyObject
                    if (p.child == ffi.PyObject) {
                        return .{ .py = obj };
                    }

                    if (State.findDefinition(p.child)) |def| {
                        // If the pointer is for a Pydust class
                        if (def.type == .class) {
                            const PyType = pytypes.PyTypeStruct(p.child);
                            const ffiObject: *ffi.PyObject = @constCast(@ptrCast(@fieldParentPtr(PyType, "state", obj)));
                            return .{ .py = ffiObject };
                        }

                        // If the pointer is for a Pydust module
                        if (def.type == .module) {
                            @compileError("Cannot currently return modules");
                        }
                    }
                },
                .Struct => {
                    // Support all extensions of py.PyObject, e.g. py.PyString, py.PyFloat
                    if (@hasField(T, "obj") and @hasField(std.meta.fieldInfo(T, .obj).type, "py")) {
                        return obj.obj;
                    }
                    if (T == py.PyObject) {
                        return obj;
                    }
                },
                inline else => {},
            }
            @compileError("Cannot convert into PyObject: " ++ @typeName(T));
        }

        inline fn isObjectLike() bool {
            switch (@typeInfo(T)) {
                .Pointer => |p| {
                    // The object is an ffi.PyObject
                    if (p.child == ffi.PyObject) {
                        return true;
                    }

                    if (State.findDefinition(p.child)) |_| {
                        return true;
                    }
                },
                .Struct => {
                    // Support all extensions of py.PyObject, e.g. py.PyString, py.PyFloat
                    if (@hasField(T, "obj") and @hasField(std.meta.fieldInfo(T, .obj).type, "py")) {
                        return true;
                    }

                    // Support py.PyObject
                    if (T == py.PyObject) {
                        return true;
                    }
                },
                inline else => {},
            }
            return false;
        }

        /// Wraps a Zig object into a Python object.
        /// Always creates a new strong reference.
        pub inline fn wrapNew(obj: T) PyError!py.PyObject {
            // For existing object types, we just incref and return the object.
            if (isObjectLike()) {
                const pyobj = asObject(obj);
                pyobj.incref();
                return pyobj;
            }

            // Since we're allowed to create a new reference, we can support string conversions
            switch (@typeInfo(T)) {
                .Pointer => |p| {
                    // We make the assumption that []const u8 is converted to a PyUnicode.
                    if (p.child == u8 and p.size == .Slice and p.is_const) {
                        return (try py.PyString.create(obj)).obj;
                    }

                    // Also pointers to u8 arrays *[_]u8
                    const childInfo = @typeInfo(p.child);
                    if (childInfo == .Array and childInfo.Array.child == u8) {
                        return (try py.PyString.create(obj)).obj;
                    }
                },
                else => {},
            }

            return wrap(obj);
        }

        /// Wraps a Zig object into a Python object.
        /// Does not create a new reference.
        pub inline fn wrap(obj: T) PyError!py.PyObject {
            // Check the user is not accidentally returning a Pydust class or Module without a pointer
            if (State.findDefinition(T) != null) {
                @compileError("Pydust objects can only be returned as pointers");
            }

            const typeInfo = @typeInfo(T);

            // Early return to handle errors
            if (typeInfo == .ErrorUnion) {
                const value = coerceError(obj) catch |err| return err;
                return Trampoline(typeInfo.ErrorUnion.payload).wrap(value);
            }

            // Early return to handle optionals
            if (typeInfo == .Optional) {
                const value = obj orelse return py.None();
                return Trampoline(typeInfo.Optional.child).wrap(value);
            }

            // Shortcut for object types
            if (isObjectLike()) {
                return asObject(obj);
            }

            switch (@typeInfo(T)) {
                .Bool => return if (obj) py.True().obj else py.False().obj,
                .ErrorUnion => @compileError("ErrorUnion already handled"),
                .Float => return (try py.PyFloat.create(obj)).obj,
                .Int => return (try py.PyLong.create(obj)).obj,
                .Pointer => {
                    // We cannot wrap a []const u8 since PyString.create will make a copy of the string
                    // and we have no way of de-allocating the original slice.
                },
                .Struct => |s| {
                    // When recursively converting to tuple or dict, Pydust will either create a new Python object
                    // or use the existing one. To avoid double-counting existing objects when wrapping up in tuple or dict,
                    // we decref each of the existing struct fields. The Trampoline.decref_objectlike function will
                    // only decref objects that already look like Python objects.
                    defer decref_objectlike(obj);

                    // If the struct is a tuple, convert into a Python tuple
                    if (s.is_tuple) {
                        return (try py.PyTuple.create(obj)).obj;
                    }

                    // Otherwise, return a Python dictionary
                    return (try py.PyDict.create(obj)).obj;
                },
                .Void => return py.None(),
                else => {},
            }

            @compileError("Unsupported return type " ++ @typeName(T));
        }

        /// Unwrap a Python object into a Zig object. Does not steal a reference.
        /// The Python object must be the correct corresponding type (vs a cast which coerces values).
        pub inline fn unwrap(object: ?py.PyObject) PyError!T {
            // Handle the error case explicitly, then we can unwrap the error case entirely.
            const typeInfo = @typeInfo(T);

            // Early return to handle errors
            if (typeInfo == .ErrorUnion) {
                const value = coerceError(object) catch |err| return err;
                return @as(T, Trampoline(typeInfo.ErrorUnion.payload).unwrap(value));
            }

            // Early return to handle optionals
            if (typeInfo == .Optional) {
                const value = object orelse return null;
                if (py.is_none(value)) return null;
                return @as(T, try Trampoline(typeInfo.Optional.child).unwrap(value));
            }

            // Otherwise we can unwrap the object.
            var obj = object orelse @panic("Unexpected null");

            switch (@typeInfo(T)) {
                .Bool => return (try py.PyBool.checked(obj)).asbool(),
                .ErrorUnion => @compileError("ErrorUnion already handled"),
                .Float => return try (try py.PyFloat.checked(obj)).as(T),
                .Int => return try (try py.PyLong.checked(obj)).as(T),
                .Optional => @compileError("Optional already handled"),
                .Pointer => |p| {
                    if (State.findDefinition(p.child)) |def| {
                        // If the pointer is for a Pydust module
                        if (def.type == .module) {
                            const mod = try py.PyModule.checked(obj);
                            return try mod.getState(p.child);
                        }

                        // If the pointer is for a Pydust class
                        if (def.type == .class) {
                            const Cls = try py.self(p.child);
                            if (!try py.isinstance(obj, Cls)) {
                                const clsName = State.getIdentifier(p.child).name;
                                const mod = State.getContaining(p.child, .module);
                                const modName = State.getIdentifier(mod).name;
                                return py.TypeError.raiseFmt(
                                    "Expected {s}.{s} but found {s}",
                                    .{ modName, clsName, try obj.getTypeName() },
                                );
                            }

                            const PyType = pytypes.PyTypeStruct(p.child);
                            const pyobject = @as(*PyType, @ptrCast(obj.py));
                            return @constCast(&pyobject.state);
                        }
                    }

                    // We make the assumption that []const u8 is converted from a PyString
                    if (p.child == u8 and p.size == .Slice and p.is_const) {
                        return (try py.PyString.checked(obj)).asSlice();
                    }

                    @compileError("Unsupported pointer type " ++ @typeName(p.child));
                },
                .Struct => |s| {
                    // Support all extensions of py.PyObject, e.g. py.PyString, py.PyFloat
                    if (@hasField(T, "obj") and @hasField(std.meta.fieldInfo(T, .obj).type, "py")) {
                        return try @field(T, "checked")(obj);
                    }
                    // Support py.PyObject
                    if (T == py.PyObject and @TypeOf(obj) == py.PyObject) {
                        return obj;
                    }
                    // If the struct is a tuple, extract from the PyTuple
                    if (s.is_tuple) {
                        return (try py.PyTuple.checked(obj)).as(T);
                    }
                    // Otherwise, extract from a Python dictionary
                    return (try py.PyDict.checked(obj)).as(T);
                },
                .Void => if (py.is_none(obj)) return else return py.TypeError.raise("expected None"),
                else => {},
            }

            @compileError("Unsupported argument type " ++ @typeName(T));
        }

        pub const CallArgs = struct {
            args: ?py.PyTuple,
            kwargs: ?py.PyDict,

            pub fn nargs(self: CallArgs) usize {
                return if (self.args) |args| args.length() else 0;
            }

            pub fn nkwargs(self: CallArgs) usize {
                return if (self.kwargs) |kwargs| kwargs.length() else 0;
            }

            pub fn getArg(self: CallArgs, comptime R: type, idx: usize) !R {
                const args = self.args orelse return py.TypeError.raise("missing args");
                return try args.getItem(R, idx);
            }

            pub fn getKwarg(self: CallArgs, comptime R: type, name: []const u8) !?R {
                const kwargs = self.kwargs orelse return null;
                return kwargs.getItem(R, name);
            }

            pub fn decref(self: CallArgs) void {
                if (self.args) |args| args.decref();
                if (self.kwargs) |kwargs| kwargs.decref();
            }
        };

        /// Wrap a Zig Pydust argument struct into Python CallArgs.
        /// Creates new references.
        pub inline fn wrapCallArgs(obj: T) !CallArgs {
            const args = try py.PyTuple.new(funcs.argCount(T));
            const kwargs = try py.PyDict.new();

            inline for (@typeInfo(T).Struct.fields, 0..) |field, i| {
                const arg = try Trampoline(field.type).wrapNew(@field(obj, field.name));
                if (field.default_value == null) {
                    // It's an arg
                    try args.setOwnedItem(i, arg);
                } else {
                    // It's a kwarg
                    try kwargs.setOwnedItemStr(field.name, arg);
                }
            }

            return .{ .args = args, .kwargs = kwargs };
        }

        pub inline fn unwrapCallArgs(callArgs: CallArgs) PyError!T {
            if (funcs.argCount(T) != callArgs.nargs()) {
                return py.TypeError.raiseComptimeFmt(
                    "expected {d} argument{s}",
                    .{ funcs.argCount(T), if (funcs.argCount(T) > 1) "s" else "" },
                );
            }

            var args: T = undefined;
            inline for (@typeInfo(T).Struct.fields, 0..) |field, i| {
                if (field.default_value) |def| {
                    // We're a kwarg
                    if (try callArgs.getKwarg(field.type, field.name)) |kwarg| {
                        @field(args, field.name) = kwarg;
                    } else {
                        @field(args, field.name) = @as(*field.type, @constCast(@alignCast(@ptrCast(def)))).*;
                    }
                } else {
                    // We're an arg
                    @field(args, field.name) = try callArgs.getArg(field.type, i);
                }
            }

            // Sanity check that we didn't recieve any kwargs that we weren't expecting
            const fieldNames = std.meta.fieldNames(T);
            if (callArgs.kwargs) |kwargs| {
                var iter = kwargs.itemsIterator();
                while (iter.next()) |item| {
                    const itemName = try (try item.key(py.PyString)).asSlice();

                    var exists = false;
                    for (fieldNames) |name| {
                        if (std.mem.eql(u8, name, itemName)) {
                            exists = true;
                            break;
                        }
                    }

                    if (!exists) {
                        return py.TypeError.raiseFmt("unexpected kwarg '{s}'", .{itemName});
                    }
                }
            }

            return args;
        }
    };
}

/// Takes a value that optionally errors and coerces it always into a PyError.
pub fn coerceError(result: anytype) coerceErrorType(@TypeOf(result)) {
    const typeInfo = @typeInfo(@TypeOf(result));
    if (typeInfo == .ErrorUnion) {
        return result catch |err| {
            if (err == PyError.PyRaised) return PyError.PyRaised;
            if (err == PyError.OutOfMemory) return PyError.OutOfMemory;
            return py.RuntimeError.raise(@errorName(err));
        };
    } else {
        return result;
    }
}

fn coerceErrorType(comptime Result: type) type {
    const typeInfo = @typeInfo(Result);
    if (typeInfo == .ErrorUnion) {
        // Unwrap the error to ensure it's a PyError
        return PyError!typeInfo.ErrorUnion.payload;
    } else {
        // Always return a PyError union so the caller can always "try".
        return PyError!Result;
    }
}
