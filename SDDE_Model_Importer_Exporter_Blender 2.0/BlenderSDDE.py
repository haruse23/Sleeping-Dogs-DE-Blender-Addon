import bpy
import os
import importlib
import mathutils
import sys
import io
import math
import struct


from .SDDE_OOP import *

LOOKUP_TABLE = """00 00 00 00 B7 1D C1 04 6E 3B 82 09 D9 26 43 0D DC 76 04 13 6B 6B C5 17 B2 4D 86 1A 05 50 47 1E B8 ED 08 26 0F F0 C9 22 D6 D6 8A 2F 61 CB 4B 2B 64 9B 0C 35 D3 86 CD 31 0A A0 8E 3C BD BD 4F 38 70 DB 11 4C C7 C6 D0 48 1E E0 93 45 A9 FD 52 41 AC AD 15 5F 1B B0 D4 5B C2 96 97 56 75 8B 56 52 C8 36 19 6A 7F 2B D8 6E A6 0D 9B 63 11 10 5A 67 14 40 1D 79 A3 5D DC 7D 7A 7B 9F 70 CD 66 5E 74 E0 B6 23 98 57 AB E2 9C 8E 8D A1 91 39 90 60 95 3C C0 27 8B 8B DD E6 8F 52 FB A5 82 E5 E6 64 86 58 5B 2B BE EF 46 EA BA 36 60 A9 B7 81 7D 68 B3 84 2D 2F AD 33 30 EE A9 EA 16 AD A4 5D 0B 6C A0 90 6D 32 D4 27 70 F3 D0 FE 56 B0 DD 49 4B 71 D9 4C 1B 36 C7 FB 06 F7 C3 22 20 B4 CE 95 3D 75 CA 28 80 3A F2 9F 9D FB F6 46 BB B8 FB F1 A6 79 FF F4 F6 3E E1 43 EB FF E5 9A CD BC E8 2D D0 7D EC 77 70 86 34 C0 6D 47 30 19 4B 04 3D AE 56 C5 39 AB 06 82 27 1C 1B 43 23 C5 3D 00 2E 72 20 C1 2A CF 9D 8E 12 78 80 4F 16 A1 A6 0C 1B 16 BB CD 1F 13 EB 8A 01 A4 F6 4B 05 7D D0 08 08 CA CD C9 0C 07 AB 97 78 B0 B6 56 7C 69 90 15 71 DE 8D D4 75 DB DD 93 6B 6C C0 52 6F B5 E6 11 62 02 FB D0 66 BF 46 9F 5E 08 5B 5E 5A D1 7D 1D 57 66 60 DC 53 63 30 9B 4D D4 2D 5A 49 0D 0B 19 44 BA 16 D8 40 97 C6 A5 AC 20 DB 64 A8 F9 FD 27 A5 4E E0 E6 A1 4B B0 A1 BF FC AD 60 BB 25 8B 23 B6 92 96 E2 B2 2F 2B AD 8A 98 36 6C 8E 41 10 2F 83 F6 0D EE 87 F3 5D A9 99 44 40 68 9D 9D 66 2B 90 2A 7B EA 94 E7 1D B4 E0 50 00 75 E4 89 26 36 E9 3E 3B F7 ED 3B 6B B0 F3 8C 76 71 F7 55 50 32 FA E2 4D F3 FE 5F F0 BC C6 E8 ED 7D C2 31 CB 3E CF 86 D6 FF CB 83 86 B8 D5 34 9B 79 D1 ED BD 3A DC 5A A0 FB D8 EE E0 0C 69 59 FD CD 6D 80 DB 8E 60 37 C6 4F 64 32 96 08 7A 85 8B C9 7E 5C AD 8A 73 EB B0 4B 77 56 0D 04 4F E1 10 C5 4B 38 36 86 46 8F 2B 47 42 8A 7B 00 5C 3D 66 C1 58 E4 40 82 55 53 5D 43 51 9E 3B 1D 25 29 26 DC 21 F0 00 9F 2C 47 1D 5E 28 42 4D 19 36 F5 50 D8 32 2C 76 9B 3F 9B 6B 5A 3B 26 D6 15 03 91 CB D4 07 48 ED 97 0A FF F0 56 0E FA A0 11 10 4D BD D0 14 94 9B 93 19 23 86 52 1D 0E 56 2F F1 B9 4B EE F5 60 6D AD F8 D7 70 6C FC D2 20 2B E2 65 3D EA E6 BC 1B A9 EB 0B 06 68 EF B6 BB 27 D7 01 A6 E6 D3 D8 80 A5 DE 6F 9D 64 DA 6A CD 23 C4 DD D0 E2 C0 04 F6 A1 CD B3 EB 60 C9 7E 8D 3E BD C9 90 FF B9 10 B6 BC B4 A7 AB 7D B0 A2 FB 3A AE 15 E6 FB AA CC C0 B8 A7 7B DD 79 A3 C6 60 36 9B 71 7D F7 9F A8 5B B4 92 1F 46 75 96 1A 16 32 88 AD 0B F3 8C 74 2D B0 81 C3 30 71 85 99 90 8A 5D 2E 8D 4B 59 F7 AB 08 54 40 B6 C9 50 45 E6 8E 4E F2 FB 4F 4A 2B DD 0C 47 9C C0 CD 43 21 7D 82 7B 96 60 43 7F 4F 46 00 72 F8 5B C1 76 FD 0B 86 68 4A 16 47 6C 93 30 04 61 24 2D C5 65 E9 4B 9B 11 5E 56 5A 15 87 70 19 18 30 6D D8 1C 35 3D 9F 02 82 20 5E 06 5B 06 1D 0B EC 1B DC 0F 51 A6 93 37 E6 BB 52 33 3F 9D 11 3E 88 80 D0 3A 8D D0 97 24 3A CD 56 20 E3 EB 15 2D 54 F6 D4 29 79 26 A9 C5 CE 3B 68 C1 17 1D 2B CC A0 00 EA C8 A5 50 AD D6 12 4D 6C D2 CB 6B 2F DF 7C 76 EE DB C1 CB A1 E3 76 D6 60 E7 AF F0 23 EA 18 ED E2 EE 1D BD A5 F0 AA A0 64 F4 73 86 27 F9 C4 9B E6 FD 09 FD B8 89 BE E0 79 8D 67 C6 3A 80 D0 DB FB 84 D5 8B BC 9A 62 96 7D 9E BB B0 3E 93 0C AD FF 97 B1 10 B0 AF 06 0D 71 AB DF 2B 32 A6 68 36 F3 A2 6D 66 B4 BC DA 7B 75 B8 03 5D 36 B5 B4 40 F7 B1"""

LOOKUP_TABLE = bytes(int(b, 16) for b in LOOKUP_TABLE.split())

TABLE_UNPACKED = list(struct.unpack("<256I", LOOKUP_TABLE))


def Custom_Hash_Function(s, seed=0xFFFFFFFF): # The hash function used by the game
    h = seed
    for c in s:
        c = ord(c)
        if 0x61 <= c <= 0x7A:  # a-z
            c -= 0x20
        index = ((h >> 24) ^ c) & 0xFF
        h = ((h << 8) & 0xFFFFFFFF) ^ TABLE_UNPACKED[index]
    return h



def get_used_bones(collection_name):
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        return []

    armature = next((obj for obj in collection.objects if obj.type == 'ARMATURE'), None)
    if not armature:
        return []

    used_bones = set()
    meshes = [obj for obj in collection.objects if obj.type == 'MESH']

    for mesh in meshes:
        for vert in mesh.data.vertices:
            for g in vert.groups:
                vg_name = mesh.vertex_groups[g.group].name
                if vg_name in armature.data.bones and g.weight > 0:
                    used_bones.add(vg_name)

    return list(used_bones)


def align_to_16(out):
    pos = out.tell()
    padding = (16 - (pos % 16)) % 16
    out.write(b'\x00' * padding)
    
    return padding


def write_material_chunk(mesh_name):
    Mat = io.BytesIO()
    
    paddingMat = struct.pack("<I", align_to_16(Mat))
    
    Mat.write(b'\x00' * 24)
    
    MaterialNameHash = Custom_Hash_Function(mesh_name)
    
    Mat.write(struct.pack("<I", MaterialNameHash))
    
    Mat.write(b'\x00' * 20)
    
    MaterialNameMarker = b'\x12\x63\xC2\xB4'
    
                
    Mat.write(MaterialNameMarker)
    
    MaterialName = mesh_name.encode('ascii') + b'\x00' * (36 - len(mesh_name))

    
    Mat.write(MaterialName)
    
    
    hex_string = """
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 09 00 00 00 00 00 00 00 08 02 00 00 00 00 00 00 34 C9 19 5C 34 C9 19 5C 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A0 8C 1D 3C 00 00 00 00 A1 61 55 8B 00 00 00 00 8F 74 98 EB 8F 74 98 EB 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF 00 00 00 00 F2 00 C8 12 00 00 00 00 85 7A BC AC 85 7A BC AC 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 2E 10 C7 23 00 00 00 00 F2 C7 04 4D 00 00 00 00 89 66 E0 DC 53 74 37 C8 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 74 3C F1 6C 00 00 00 00 BF FA 43 8B 00 00 00 00 C7 0E 46 CB 53 74 37 C8 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 B7 A7 3E 00 00 00 00 BF FA 43 8B 00 00 00 00 5A 1A BE AD 53 74 37 C8 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A2 EA 7B 43 00 00 00 00 BF FA 43 8B 00 00 00 00 69 2F 7E 2C 53 74 37 C8 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 C6 02 7D 15 00 00 00 00 BF FA 43 8B 00 00 00 00 F1 F1 2F AA 53 74 37 C8 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 EB 69 13 B1 00 00 00 00 BF FA 43 8B 00 00 00 00 E6 65 C2 C0 E6 65 C2 C0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF 00 00 00 00 E0 15 C7 3B 00 00 00 00 00 00 00 00 00 00 00 00 1F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    """
    # Remove whitespace and convert to bytes
    data = bytes(int(b, 16) for b in hex_string.split())
    
    Mat.write(data)
 
    
    return paddingMat, Mat.getvalue(), MaterialNameHash
    
    
    
def write_bone_palette(collection_name, bone_names):
    BP = io.BytesIO()
    
    bone_count = len(bone_names) 
    
    
    BoneIndexMap = { name: i for i, name in enumerate(bone_names) }


    paddingBP = struct.pack("<I", align_to_16(BP))
    
    BP.write(b'\x00' * 24)
    
    BonePaletteID = Custom_Hash_Function(collection_name + ".BonePalette")
    
    BP.write(struct.pack("<I", BonePaletteID))
    
    BP.write(b'\x00' * 20)
    
    BonePaletteNameMarker = b'\xE3\x19\xA8\x50'
    
    BP.write(BonePaletteNameMarker)
    
    base = (collection_name + ".BonePalette").encode('ascii')
    
    BonePaletteName =  base + b'\x00' * (36 - len(base))

    
    BP.write(BonePaletteName)
    
    BP.write(b'\x01\x00\x00\x00')
    
    BP.write(struct.pack("<I", bone_count))
    
    OffsetBoneNameTablePos = BP.tell()
    
    BP.write(b'\x00' * 8)
    
    OffsetFirstBoneIDTablePos = BP.tell()
    
    BP.write(b'\x00' * 8)
    
    OffsetSecondBoneIDTablePos = BP.tell()
    
    BP.write(b'\x00' * 8)
    
    align_to_16(BP)    
    
    for byte in range(bone_count): # Bone Palette Index           
        BP.write(struct.pack("B", byte))
        
    
    for j in range(160 - bone_count):
        byte = b'\xFF'
        
        BP.write(byte)
        
     
    BoneIndicesEnd = BP.tell()
     
        
    
    for k in range(bone_count):
        name_written = bone_names[k].encode('ascii') + b'\x00' * (64 - len(bone_names[k]))
        
        BP.write(name_written)
        
    BoneNameTableEnd = BP.tell()   
        
    for l in range(bone_count):
        BoneID = Custom_Hash_Function(bone_names[l])
        
        BP.write(struct.pack("<I", BoneID))
        
    
    FirstBoneIDTableEnd = BP.tell()
    
    for l2 in range(bone_count):
        BoneID = Custom_Hash_Function(bone_names[l2])
        
        BP.write(struct.pack("<I", BoneID))
        
    
    Return = BP.tell() # To Return here and Align to 16
    
    
    OffsetBoneNameTable = BoneIndicesEnd - OffsetBoneNameTablePos
    BP.seek(OffsetBoneNameTablePos, 0)
    BP.write(struct.pack("<I", OffsetBoneNameTable))
    
    
    OffsetFirstBoneIDTable = BoneNameTableEnd - OffsetFirstBoneIDTablePos
    BP.seek(OffsetFirstBoneIDTablePos, 0)
    BP.write(struct.pack("<I", OffsetFirstBoneIDTable))
    
    
    OffsetSecondBoneNameTable = FirstBoneIDTableEnd - OffsetSecondBoneIDTablePos
    BP.seek(OffsetSecondBoneIDTablePos, 0)
    BP.write(struct.pack("<I", OffsetSecondBoneNameTable))
    

    BP.seek(Return, 0)
    
    return paddingBP, BP.getvalue(), BonePaletteID, BoneIndexMap
    
def write_index_buffer(collection_name, mesh_objs):
    IB = io.BytesIO()
    
    vertex_offset = 0
    Indices = []
    IndexCounts = []

    for mesh_obj in mesh_objs:
        mesh_indices = []
        for poly in mesh_obj.data.polygons:
            # add vertex_offset to each vertex index
            mesh_indices.extend([v + vertex_offset for v in poly.vertices])
        IndexCounts.append(len(mesh_indices))
        Indices.extend(mesh_indices)
        
        # increase offset for the next mesh
        vertex_offset += len(mesh_obj.data.vertices)

    
    TotalIndexCount = sum(IndexCounts)
    
    PrimitiveCounts = [ic // 3 for ic in IndexCounts]
    PrimitiveCount = sum(PrimitiveCounts)
    
    paddingIB = struct.pack("<I", align_to_16(IB))
    
    IB.write(b'\x00' * 24)
    
    IndexBufferID = Custom_Hash_Function(collection_name + ".IndexBuffer")
    
    IB.write(struct.pack("<I", IndexBufferID))
    
    IB.write(b'\x00' * 20)
    
    IndexBufferNameMarker = b'\x8F\xEC\xCD\x92'
    
    IB.write(IndexBufferNameMarker)
    
    base = (collection_name + ".IndexBuffer").encode('ascii')
    
    IndexBufferName =  base + b'\x00' * (36 - len(base))

    
    IB.write(IndexBufferName)
    
    IB.write(b'\x01\x00\x00\x00')
    
    IB.write(struct.pack("<I", TotalIndexCount * 2)) # NumBytes
    
    IB.write(b'\xD0\x00\x00\x00\x00\x00\x00\x00')
    
    IB.write(struct.pack("<I", 2)) # IndexStride
    
    IB.write(struct.pack("<I", TotalIndexCount)) # IndexCount
    
    
    
    
    
    
    bytes_preserved = bytes([
        0xA0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x4D, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC6, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        
    ])

    
    IB.write(bytes_preserved)
    
    
    for I in range(TotalIndexCount):
        Index = struct.pack("<H", Indices[I])
        
        IB.write(Index)
    
    align_to_16(IB)
    
    return paddingIB, bytes_preserved, IB.getvalue(), IndexBufferID, PrimitiveCount, IndexCounts
    
    
    
def write_vertex_buffer(collection_name, buffer_index, VertexStride, bytes_preserved, mesh_objs, BoneIndexMap):
    VB = io.BytesIO()
 
    TotalVertexCount = sum(len(m.data.vertices) for m in mesh_objs)

    paddingVB = b'\x00' * 4
    
    VB.write(b'\x00' * 24)

    buffer_id = Custom_Hash_Function(f"{collection_name}.VertexBuffer{buffer_index}.0")
    VB.write(struct.pack("<I", buffer_id))
    
    VB.write(b'\x00' * 20)
    VB.write(b'\x8F\xEC\xCD\x92')

    name_base = f"{collection_name}.VertexBuffer{buffer_index}.0".encode('ascii')
    VB.write(name_base + b'\x00' * (36 - len(name_base)))
    
    VB.write(b'\x01\x00\x00\x00')
    
    VB.write(struct.pack("<I", TotalVertexCount * VertexStride))
    
    VB.write(b'\xD0\x00\x00\x00\x00\x00\x00\x00')
    
    VB.write(struct.pack("<I", VertexStride))
    
    VB.write(struct.pack("<I", TotalVertexCount))
        
    VB.write(bytes_preserved)

    AABBMin = [math.inf, math.inf, math.inf]
    AABBMax = [-math.inf, -math.inf, -math.inf]
    
    # Per-model AABB
    for mesh_obj in mesh_objs:
        for vertex in mesh_obj.data.vertices:
            x, y, z = vertex.co.x, vertex.co.y, vertex.co.z

            AABBMin[0] = min(AABBMin[0], x)
            AABBMin[1] = min(AABBMin[1], y)
            AABBMin[2] = min(AABBMin[2], z)

            AABBMax[0] = max(AABBMax[0], x)
            AABBMax[1] = max(AABBMax[1], y)
            AABBMax[2] = max(AABBMax[2], z)

    if buffer_index == 0:
        for mesh_obj in mesh_objs:
            mesh_obj.data.calc_tangents()
            for V in mesh_obj.data.vertices:
                positions = struct.pack("<4f", V.co.x, V.co.y, V.co.z, 0.0)
                
                VB.write(positions)
                
                nx = int(V.normal.x * 127)
                ny = int(V.normal.y * 127)
                nz = int(V.normal.z * 127)
                nw = 0

                normals = struct.pack("4b", nx, ny, nz, nw)
                VB.write(normals)
                
                loop_index = V.index
                tangents = mesh_obj.data.loops[loop_index].tangent
                
                tx = int(tangents.x * 127)
                ty = int(tangents.y * 127)
                tz = int(tangents.z * 127)
                tw = 0

                tangents = struct.pack("4b", tx, ty, tz, tw)
                VB.write(tangents)
  

        align_to_16(VB)
  
    
   
       
   
    if buffer_index == 1:
        max_influences = 4
        for mesh_obj in mesh_objs:
            for vertex in mesh_obj.data.vertices:
                bone_indices = [0] * max_influences
                bone_weights = [0] * max_influences

                for gi, g in enumerate(vertex.groups):
                    if gi >= max_influences:
                        break
                    group_name = mesh_obj.vertex_groups[g.group].name
                    if group_name in BoneIndexMap:
                        bone_indices[gi] = BoneIndexMap[group_name]
                        bone_weights[gi] = int(g.weight * 255)

                VB.write(struct.pack("4B", *bone_indices))
                VB.write(struct.pack("4B", *bone_weights))

        
        align_to_16(VB)
        
        

        
    
    if buffer_index == 2:
        for mesh_obj in mesh_objs:
            VertexCount = len(mesh_obj.data.vertices)
            vertex_uvs = [None] * VertexCount
            uv_layer = mesh_obj.data.uv_layers.active.data
            # Assign first UV per vertex
            for poly in mesh_obj.data.polygons:
                for loop_index in poly.loop_indices:
                    vert_idx = mesh_obj.data.loops[loop_index].vertex_index
                    if vertex_uvs[vert_idx] is None:
                        vertex_uvs[vert_idx] = uv_layer[loop_index].uv

            # Fill missing UVs with (0,0)
            for idx in range(VertexCount):
                if vertex_uvs[idx] is None:
                    vertex_uvs[idx] = Vector((0.0, 0.0))

            # Write UVs
            for uv in vertex_uvs:
                VB.write(struct.pack("<e", uv.x))
                VB.write(struct.pack("<e", uv.y))


        align_to_16(VB)
                
    
    return paddingVB, VB.getvalue(), buffer_id, AABBMin, AABBMax



def write_model_table(collection_name, BonePaletteID, mesh_count, MaterialNameHash, VertexDeclarationID, IndexBufferID, VertexBuffer_0_ID, VertexBuffer_1_ID, VertexBuffer_2_ID, PrimitiveCount, AABBMin, AABBMax, IndexCounts):
    MT = io.BytesIO()
    
    paddingMT = b'\x00' * 4
    
    MT.write(b'\x00' * 24)
    
    ModelNameHash = Custom_Hash_Function(collection_name)
    
    MT.write(struct.pack("<I", ModelNameHash))
    
    MT.write(b'\x00' * 20)
    
    ModelTableNameMarker = b'\x77\xCD\xAD\xA2'
    
    MT.write(ModelTableNameMarker)
    
    ModelName = collection_name.encode('ascii') + b'\x00' * (36 - len(collection_name))
    
    MT.write(ModelName)
    
    
    
    MT.write(struct.pack("<3f", *AABBMin))
    
    MT.write(struct.pack("<I", PrimitiveCount))
    
    MT.write(struct.pack("<3f", *AABBMax))
    
    MT.write(b'\x00' * 60)
    
    MT.write(struct.pack("<I", BonePaletteID))
    
    MT.write(b'\x00' * 4)
    
    MT.write(b'\xA8\x00\x00\x00\x00\x00\x00\x00')
    
    MT.write(struct.pack("<Q", mesh_count))
    
    MT.write(b'\x88\x00\x00\x00\x00\x00\x00\x00')
    
    MT.write(b'\x00' * 96)
    
    bytes_preserved = bytes([
        0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ])
    
    
    MT.write(bytes_preserved)


    save_posFinalBlockStart = MT.tell()
    MT.write(b'\x00\x00\x00\x00')  # FinalBlockSize placeholder
    MT.write(b'\x00' * 12) 

    offset_after_offsets_list = save_posFinalBlockStart + 16 + mesh_count * 8

    padding = (16 - (offset_after_offsets_list % 16)) % 16

    MeshTableStart = offset_after_offsets_list + padding

      

    mesh_offsets = []
    offset_field_pos = MeshTableStart
    
    for mesh_index in range(mesh_count):
        rel_offset = offset_field_pos - (save_posFinalBlockStart + 16)
        
        rel_offset = rel_offset - mesh_index * 8

        mesh_offsets.append(rel_offset)
       
        offset_field_pos += 272  

       

    for mo in mesh_offsets:
        MT.write(struct.pack("<Q", mo))
        
    MT.write(b'\x00' * padding)
    
    current_mesh_position = 0
    
    for mi in range(mesh_count):
        MT.write(b'\x00' * 24)
        MT.write(struct.pack("<I", MaterialNameHash))
        
        MT.write(b'\x00' * 28 )
        MT.write(struct.pack("<I", VertexDeclarationID))
        
        MT.write(b'\x00' * 28 )
        MT.write(struct.pack("<I", IndexBufferID))
        
        MT.write(b'\x00' * 28 )
        MT.write(struct.pack("<I", VertexBuffer_0_ID))
        
        MT.write(b'\x00' * 28 )
        MT.write(struct.pack("<I", VertexBuffer_1_ID))
        
        MT.write(b'\x00' * 28 )
        MT.write(struct.pack("<I", VertexBuffer_2_ID))
        
        MT.write(b'\x00' * 36)
        MT.write(struct.pack("<I", 3)) # Always 03 00 00 00 -- NumPrimitives -- 3 = Triangles
        
        
        
        MT.write(struct.pack("<I", current_mesh_position))
            
        MT.write(struct.pack("<I", IndexCounts[mi] // 3)) # NumPrimitives (Triangle Count)
        
        MT.write(b'\x00' * 36)
        
        current_mesh_position += IndexCounts[mi]
    
    align_to_16(MT)
    
    save_posFinalBlockEnd = MT.tell()
    
    FinalBlockSize = save_posFinalBlockEnd - save_posFinalBlockStart
    
    MT.seek(save_posFinalBlockStart, 0)
    MT.write(struct.pack("<I", FinalBlockSize))
    
    MT.seek(save_posFinalBlockEnd, 0)
    
    return paddingMT, MT.getvalue()
    

def ImportSDDEModel(filepath):
    with open(filepath, "rb") as f:
        pattern = b'\xB3\x63\xF9\x6D'

        data = f.read()
        
        positions = []
        pos = data.find(pattern)
        while pos != -1:
            positions.append(pos)
            pos = data.find(pattern, pos + 1)
        
        Model_Tables = []
        if positions:
            print(f"Pattern found at offsets: {positions}")
            for pos in positions:
                f.seek(pos, 0)  # Seek to this model table
                chunk = Chunk(f)
                Model_Table = ModelTable(f, chunk)
                Model_Tables.append(Model_Table)
  
        else:
            print("Pattern not found")
                
            
        file_size = os.path.getsize(filepath)
        
        f.seek(0, 0)
        
        Material_Chunk_Obj = None
        Bone_Palette_Chunk_Obj = None
        Index_Buffer_Obj = None
        Vertex_Buffer_0_Obj = None
        Vertex_Buffer_1_Obj = None
        Vertex_Buffer_2_Obj = None

        Material_Chunks = []
        Bone_Palette_Chunks = []
        Index_Buffers = []
        Vertex_Buffers_0 = []
        VertexBuffer0POS = []
        
        Vertex_Buffers_1 = []
        VertexBuffer1POS = []
        
        Vertex_Buffers_2 = []
        VertexBuffer2POS = []
        
        while f.tell() < file_size:
        
            chunk = Chunk(f)
            print(chunk.ChunkID)
            print(f.tell())      
            
            
            if chunk.ChunkID == 4126691695:
                Material_Chunk_Obj = MaterialChunk(f, chunk)
                                    
                
                Material_Chunks.append(Material_Chunk_Obj)
            
            elif chunk.ChunkID == 2552518363:
                Bone_Palette_Chunk_Obj = BonePaletteChunk(f, chunk)
                
                Bone_Palette_Chunks.append(Bone_Palette_Chunk_Obj)
                
            elif chunk.ChunkID == 2056721529:
                read_into = f.read(304)

                if b'Index' in read_into:

                    f.seek(-304 - chunk.PaddingSize - 16, 1)
     
                    Index_Buffer_Obj = IndexBuffer(f, chunk)
                    
                    Index_Buffers.append(Index_Buffer_Obj)
                    
                elif b'0.0' in read_into or b'0.0.0' in read_into:

                    f.seek(-304 - chunk.PaddingSize - 16, 1)

                    VertexBuffer0POS.append(f.tell())
                    
                    Vertex_Buffer_0_Obj = f.read(chunk.ChunkSize + 16)
                    
                    Vertex_Buffers_0.append(Vertex_Buffer_0_Obj)
                    
                elif b'1.0' in read_into or b'0.0.1' in read_into:
                    f.seek(-304 - chunk.PaddingSize - 16, 1)
                        
                    VertexBuffer1POS.append(f.tell())
                    
                    Vertex_Buffer_1_Obj = f.read(chunk.ChunkSize + 16)
                    
                    Vertex_Buffers_1.append(Vertex_Buffer_1_Obj)
                    
                elif b'2.0' in read_into or b'0.0.2' in read_into:
                    f.seek(-304 - chunk.PaddingSize - 16, 1)

                    VertexBuffer2POS.append(f.tell())
                    
                    Vertex_Buffer_2_Obj = f.read(chunk.ChunkSize + 16)
                    
                    Vertex_Buffers_2.append(Vertex_Buffer_2_Obj)
                    
            else:
                f.seek(chunk.ChunkSize - chunk.PaddingSize, 1)
        

        
                

        for model_index, model_table in enumerate(Model_Tables):
            
            model_collection = bpy.data.collections.new(model_table.ModelName)
            bpy.context.scene.collection.children.link(model_collection)
    
            for mesh_index in range(model_table.MeshCount):   
                
                mesh_material_id = model_table.MaterialIDs[mesh_index]
                
                matching_material = None
                
                # Find the material chunk that matches this ID
                for MC in Material_Chunks:
                    if MC.MaterialNameHash == mesh_material_id and MC.MaterialNameHash != 0:
                        matching_material = MC

                if matching_material:
                    MeshName = matching_material.MaterialName
                else:
                    MeshName = f"Model_{model_table.ModelName}_Mesh_{mesh_index}"
                    
                
                BonePalette = None
                Index_Buffer = None
                Vertex_Buffer0 = None
                Vertex_Buffer1 = None
                Vertex_Buffer2 = None
                
                VertexDeclarationID = model_table.VertexDeclarationIDs[mesh_index]
                BonePaletteID = model_table.BonePaletteID
                IndexBufferID = model_table.IndexBufferIDs[mesh_index] # The correct one for every mesh in every model, same for the other chunks
                VertexBuffer0ID = model_table.Vertex_Buffer0IDs[mesh_index]
                VertexBuffer1ID = model_table.Vertex_Buffer1IDs[mesh_index]
                VertexBuffer2ID = model_table.Vertex_Buffer2IDs[mesh_index]
                
                for BP in Bone_Palette_Chunks:
                        if BP.BonePaletteID == BonePaletteID:
                            BonePalette = BP
                            
                    
                for IB in Index_Buffers:
                    if IndexBufferID != 0 and IB.IndexBufferID == IndexBufferID:
                        Index_Buffer = IB

                # Vertex Buffer 0
                for i, V0 in enumerate(Vertex_Buffers_0):
                    if VertexBuffer0ID != 0 and VertexBuffer0ID.to_bytes(4, "little") in V0:
                        f.seek(VertexBuffer0POS[i], 0)
                        print(VertexBuffer0POS[i], "Here")
                        Vertex_Buffer0 = VertexBuffer_0(f, model_table, VertexDeclarationID)
                        if Vertex_Buffer0.VertexBuffer_0ID == VertexBuffer0ID:
                            break

                # Vertex Buffer 1
                for i, V1 in enumerate(Vertex_Buffers_1):
                    if VertexBuffer1ID != 0 and VertexBuffer1ID.to_bytes(4, "little") in V1:
                        f.seek(VertexBuffer1POS[i], 0)
                        Vertex_Buffer1 = VertexBuffer_1(f, model_table, VertexDeclarationID)
                        if Vertex_Buffer1.VertexBuffer_1ID == VertexBuffer1ID:
                            break

                # Vertex Buffer 2
                for i, V2 in enumerate(Vertex_Buffers_2):
                    if VertexBuffer2ID != 0 and VertexBuffer2ID.to_bytes(4, "little") in V2:
                        f.seek(VertexBuffer2POS[i], 0)
                        Vertex_Buffer2 = VertexBuffer_2(f, model_table, VertexDeclarationID)
                        if Vertex_Buffer2.VertexBuffer_2ID == VertexBuffer2ID:
                            break




                MeshData = bpy.data.meshes.new(MeshName)
                MeshObj = bpy.data.objects.new(MeshName, MeshData)
                
                Positions_Buffer = None
                UV_Buffers = []
                Normals_Buffer = None
                Tangents_Buffer = None
                Colors_Buffer = None
                Weights_Buffer = None
                
                for vb in [Vertex_Buffer0, Vertex_Buffer1, Vertex_Buffer2]:
                    if vb is None:
                        continue
                    
                    if hasattr(vb, "Positions") and vb.Positions and Positions_Buffer is None:
                        Positions_Buffer = vb         

                    if hasattr(vb, "UVs0") and vb.UVs0 and len(UV_Buffers) == 0:
                        UV_Buffers.append(vb.UVs0)

                    if hasattr(vb, "UVs1") and vb.UVs1 and len(UV_Buffers) == 1:
                        UV_Buffers.append(vb.UVs1)
                        
                    if hasattr(vb, "Normals") and vb.Normals and Normals_Buffer is None:
                        Normals_Buffer = vb
                        
                    if hasattr(vb, "Tangents") and vb.Tangents and Tangents_Buffer is None:
                        Tangents_Buffer = vb
                    
                    if hasattr(vb, "Colors0") and vb.Colors0 and Colors_Buffer is None:
                        Colors_Buffer = vb
                        
                    if hasattr(vb, "BlendIndicesAndWeights") and vb.BlendIndicesAndWeights:
                        all_indices = [i for vertex in vb.BlendIndicesAndWeights for i, _ in vertex]
                        all_weights = [w for vertex in vb.BlendIndicesAndWeights for _, w in vertex]
                        if 'UVNT' not in vb.VertexBuffer_1Name:
                            Weights_Buffer = vb


                        
                if Positions_Buffer is None or not hasattr(Positions_Buffer, "Positions"):
                    print(f"Skipping mesh {MeshName} because no vertex positions found")
                    continue

                
                Colors0 = None
                UVs0 = None
                UVs1 = None
                
                if Index_Buffer:
                    # Slice Indices
                    Mesh_Start = model_table.MeshPositionsInIndexBuffer[mesh_index]
                    
                    if mesh_index + 1 < len(model_table.MeshPositionsInIndexBuffer):
                        Mesh_End = model_table.MeshPositionsInIndexBuffer[mesh_index + 1]
                    else:
                        Mesh_End = len(Index_Buffer.Indices)  # last mesh uses remaining indices

                    
                    Mesh_Indices = Index_Buffer.Indices[Mesh_Start:Mesh_End]
  
                             
                    # Build mapping: global vertex index → local mesh index
                    unique_indices = list(dict.fromkeys(Mesh_Indices))  # preserve order, remove duplicates
                    vert_map = {global_idx: local_idx for local_idx, global_idx in enumerate(unique_indices)}

                    # Slice positions, UVs, colors using mesh-local indices
                    positions = [Positions_Buffer.Positions[i] for i in unique_indices]
                    UVs0 = [UV_Buffers[0][i] for i in unique_indices]
                    UVs1 = [UV_Buffers[1][i] for i in unique_indices] if len(UV_Buffers) > 1 else None
                    Colors0 = [Colors_Buffer.Colors0[i] for i in unique_indices] if Colors_Buffer else None

                    # Remap faces to local indices
                    faces = [(vert_map[Mesh_Indices[i]], vert_map[Mesh_Indices[i+1]], vert_map[Mesh_Indices[i+2]])
                             for i in range(0, len(Mesh_Indices), 3)]
                    
          
                    MeshData.from_pydata(positions, [], faces)
                    
                MeshData.update()

            
                material_name = matching_material.MaterialName if matching_material else f"Model_{model_table.ModelName}_Mesh_{mesh_index}_Material"
                material = bpy.data.materials.new(name=material_name)
                
                
                # Assign material to object
                if MeshObj.data.materials:
                    MeshObj.data.materials[0] = material
                else:
                    MeshObj.data.materials.append(material)


                for poly in MeshObj.data.polygons:
                    poly.material_index = 0

                
               
#                if Normals_Buffer:
#                    mesh_data = MeshObj.data

#                    loop_normals = [None] * len(mesh_data.loops)

#                    for poly in mesh_data.polygons:
#                        for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
#                            vertex_index = mesh_data.loops[loop_index].vertex_index
#                            nx, ny, nz = Normals_Buffer.Normals[vertex_index]
#                            loop_normals[loop_index] = (nx, ny, nz)

#                    mesh_data.normals_split_custom_set(loop_normals)
#                    mesh_data.update()

                      
                if UVs0:
                    # Add a new UV layer
                    if not MeshData.uv_layers:
                        uv_layer0 = MeshData.uv_layers.new(name="UVMap_0")
                    else:
                        uv_layer0 = MeshData.uv_layers[0]  # reuse if already exists

                    # Assign UVs per loop
                    for loop_index, loop in enumerate(MeshData.loops):
                        vert_index = loop.vertex_index
                        u, v = UVs0[vert_index]
                        uv_layer0.data[loop_index].uv = (float(u), float(v))
                
                if UVs1:
                    uv_layer1 = MeshData.uv_layers.new(name="UVMap_1")
                    for loop_index, loop in enumerate(MeshData.loops):
                        vert_index = loop.vertex_index
                        u, v = UVs1[vert_index]
                        uv_layer1.data[loop_index].uv = (float(u), float(v))



            
                
                if Colors0:
                    color_layer = MeshData.color_attributes.new(
                        name="Color",
                        type='FLOAT_COLOR',
                        domain='CORNER'
                    )

                    color_data = color_layer.data
                    for loop_index, loop in enumerate(MeshData.loops):
                        vert_index = loop.vertex_index
                        r, g, b, a = Colors0[vert_index]
                        color_data[loop_index].color = (r, g, b, a)


                MeshData.update()
                
                if Weights_Buffer and BonePalette:
                    for bone_name in BonePalette.BoneNames:
                        MeshObj.vertex_groups.new(name=bone_name)

                    for global_idx, bone_weight_list in enumerate(Weights_Buffer.BlendIndicesAndWeights):
                        if global_idx in vert_map:
                            local_idx = vert_map[global_idx]
                            for blend_index, blend_weight in bone_weight_list:
                                MeshObj.vertex_groups[blend_index].add([local_idx], blend_weight, 'ADD')

                

                model_collection.objects.link(MeshObj)
                
                bpy.context.view_layer.objects.active = MeshObj
                MeshObj.select_set(True)
                
                bpy.ops.object.shade_auto_smooth(use_auto_smooth=True, angle=3.14159)




def ExportSDDEModel(filepath):
#    filename_with_ext = os.path.basename(filepath2)
#    filename_no_ext = os.path.splitext(filename_with_ext)[0]
#    
#    output_path = os.path.join(filepath, filename_no_ext + ".perm.bin")
    
    selected_cols = [
        item.collection for item in bpy.context.scene.sdde_export_collections
        if item.selected
    ]

    if not selected_cols:
        print("No collections selected for export")
        return
                
    with open(filepath + ".perm.bin", "wb") as out:
        
        for i, collection in enumerate(selected_cols):  
            
            collection_name = collection.name
            mesh_objs = [obj for obj in collection.objects if obj.type == "MESH"]
            mesh_count = len(mesh_objs)
                
            bone_names = get_used_bones(collection_name)
            
            MaterialChunkID = struct.pack("<I", 4126691695)
           
            
            for mesh_obj in mesh_objs:
                mesh_name = mesh_obj.name
                paddingMat, MaterialChunk, MaterialNameHash= write_material_chunk(mesh_name)
                MaterialChunkLength = struct.pack("<I", len(MaterialChunk)) # Without header (16 bytes)
                out.write(MaterialChunkID)
                out.write(MaterialChunkLength)
                out.write(MaterialChunkLength)
                out.write(paddingMat)
                out.write(MaterialChunk)
                
       
            

            paddingBP, BonePalette, BonePaletteID, BoneIndexMap = write_bone_palette(collection_name, bone_names)
            
            paddingIB, bytes_preserved, IndexBuffer, IndexBufferID, PrimitiveCount, IndexCounts = write_index_buffer(collection_name, mesh_objs)
            
            paddingVB0, VertexBuffer0, VertexBuffer_0_ID, AABBMin, AABBMax = write_vertex_buffer(collection_name, 0, 24, bytes_preserved, mesh_objs, BoneIndexMap)
            
            paddingVB1, VertexBuffer1, VertexBuffer_1_ID, AABBMin, AABBMax = write_vertex_buffer(collection_name, 1, 8, bytes_preserved, mesh_objs, BoneIndexMap)
            
            paddingVB2, VertexBuffer2, VertexBuffer_2_ID, AABBMin, AABBMax = write_vertex_buffer(collection_name, 2, 4, bytes_preserved, mesh_objs, BoneIndexMap)
            
            VertexDeclarationID = 661362023
            
            paddingMT, ModelTable = write_model_table(collection_name, BonePaletteID, mesh_count, MaterialNameHash, VertexDeclarationID, IndexBufferID, VertexBuffer_0_ID, VertexBuffer_1_ID, VertexBuffer_2_ID, PrimitiveCount, AABBMin, AABBMax, IndexCounts)
            
            
            
            BonePaletteChunkID = struct.pack("<I", 2552518363)
            IndexBufferChunkID = struct.pack("<I", 2056721529)
            VertexBuffer_0_ChunkID = struct.pack("<I", 2056721529)
            VertexBuffer_1_ChunkID = struct.pack("<I", 2056721529)
            VertexBuffer_2_ChunkID = struct.pack("<I", 2056721529)
            ModelTableChunkID = struct.pack("<I", 1845060531)
            
            
            BonePaletteChunkLength = struct.pack("<I", len(BonePalette)) # Without header (16 bytes)
            IndexBufferChunkLength = struct.pack("<I", len(IndexBuffer)) # Without header (16 bytes)
            VertexBuffer_0_ChunkLength = struct.pack("<I", len(VertexBuffer0)) # Without header (16 bytes)
            VertexBuffer_1_ChunkLength = struct.pack("<I", len(VertexBuffer1)) # Without header (16 bytes)
            VertexBuffer_2_ChunkLength = struct.pack("<I", len(VertexBuffer2)) # Without header (16 bytes)
            ModelTableChunkLength = struct.pack("<I", len(ModelTable)) # Without header (16 bytes)
            
            
            
            out.write(BonePaletteChunkID)
            out.write(BonePaletteChunkLength)
            out.write(BonePaletteChunkLength)
            out.write(paddingBP)
            out.write(BonePalette)
            
            out.write(IndexBufferChunkID)
            out.write(IndexBufferChunkLength)
            out.write(IndexBufferChunkLength)
            out.write(paddingIB)
            out.write(IndexBuffer)
            
            out.write(VertexBuffer_0_ChunkID)
            out.write(VertexBuffer_0_ChunkLength)
            out.write(VertexBuffer_0_ChunkLength)
            out.write(paddingVB0)
            out.write(VertexBuffer0)
            
            out.write(VertexBuffer_1_ChunkID)
            out.write(VertexBuffer_1_ChunkLength)
            out.write(VertexBuffer_1_ChunkLength)
            out.write(paddingVB1)
            out.write(VertexBuffer1)
            
            out.write(VertexBuffer_2_ChunkID)
            out.write(VertexBuffer_2_ChunkLength)
            out.write(VertexBuffer_2_ChunkLength)
            out.write(paddingVB2)
            out.write(VertexBuffer2)
            
            out.write(ModelTableChunkID)
            out.write(ModelTableChunkLength)
            out.write(ModelTableChunkLength)
            out.write(paddingMT)
            out.write(ModelTable)            
            
            
        
       

