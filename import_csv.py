# Minimal program which imports CSV files into Blender. Tested with Blender 2.79
# 
# Copyright 2020 Jesse Kaukonen
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import bpy
import bmesh

try:
	polys = []
	cur_poly = None
	scene = bpy.context.scene

	# add the path to your CSV file here. It must be formatted as follows:
	# 1.23125,273.581289,582.1519
	# 1.7136,12.82352,18974.5787214 
	# That is, 3 floats per row followed by a newline
	f = open("/home/gekko/out.csv")
	c = 0

	verts = []

	it = 0
	c = 0
	for line in f:
		line = line.strip("\n")
		if len(line) == 0:
			continue

		parts = line.split(",")
		if len(parts) != 3:
			continue
		it = it +1
		if it % 3 != 0:
			continue

		v = ( float(parts[0]) / 1000, float(parts[1]) / 1000, float(parts[2]) / 1000)

		verts.append(v);
		c = c + 1
		if c % 10000 == 0:
			print("reading line " + str(c))
	f.close()

	mesh = bpy.data.meshes.new("points")
	obj = bpy.data.objects.new("points_object", mesh)
	scene.objects.link(obj)
	scene.objects.active = obj
	obj.select = True

	mesh = bpy.context.object.data
	bm = bmesh.new()

	for v in verts:
		if c % 10000 == 0:
			print("adding point " + str(c) + " out of " + str(len(verts)))
		c = c +1
		bm.verts.new(v)

	print("to_mesh")
	bm.to_mesh(mesh)
	print("free")
	bm.free()
except Exception as e:
	print(e)

