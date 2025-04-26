from scene.fileimport import FileImport

fileimportor = FileImport()
meshes = fileimportor.read_file("test_obj.obj")
line = fileimportor.get_data()
for mesh in meshes:
    print(str(mesh))
print(line)