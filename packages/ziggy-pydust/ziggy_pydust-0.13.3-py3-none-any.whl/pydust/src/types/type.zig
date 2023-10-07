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

const std = @import("std");
const py = @import("../pydust.zig");
const PyObjectMixin = @import("./obj.zig").PyObjectMixin;
const ffi = py.ffi;
const PyError = @import("../errors.zig").PyError;

/// Wrapper for Python PyType.
/// Since PyTypeObject is opaque in the Python API, we cannot use the PyObject mixin.
/// Instead, we re-implement the mixin functions and insert @ptrCast where necessary.
pub const PyType = extern struct {
    obj: py.PyObject,

    pub usingnamespace PyObjectMixin("type", "PyType", @This());

    pub fn name(self: PyType) !py.PyString {
        return py.PyString.unchecked(.{
            .py = ffi.PyType_GetName(typePtr(self.obj.py)) orelse return PyError.PyRaised,
        });
    }

    pub fn qualifiedName(self: PyType) !py.PyString {
        return py.PyString.unchecked(.{
            .py = ffi.PyType_GetQualName(typePtr(self.obj.py)) orelse return PyError.PyRaised,
        });
    }

    fn typePtr(obj: *ffi.PyObject) *ffi.PyTypeObject {
        return @alignCast(@ptrCast(obj));
    }

    fn objPtr(obj: *ffi.PyTypeObject) *ffi.PyObject {
        return @alignCast(@ptrCast(obj));
    }
};

test "PyType" {
    py.initialize();
    defer py.finalize();

    const io = try py.import("io");
    defer io.decref();

    const StringIO = try io.getAs(py.PyType, "StringIO");
    try std.testing.expectEqualSlices(u8, "StringIO", try (try StringIO.name()).asSlice());

    const sio = try py.call0(py.PyObject, StringIO);
    defer sio.decref();
    const sioType = try py.type_(sio);
    try std.testing.expectEqualSlices(u8, "StringIO", try (try sioType.name()).asSlice());
}
