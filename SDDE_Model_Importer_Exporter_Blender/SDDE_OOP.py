# author: haru233 

import struct
import os 
import numpy as np

def align_to_16(f):
    pos = f.tell()
    padding = (16 - (pos % 16)) % 16
    f.seek(padding, 1)
    
    return padding
    
    
class Chunk:
    def __init__(self, f):
        ChunkHeader = f.read(16)
        
        self.ChunkID = struct.unpack_from("<I", ChunkHeader, 0)[0]
        self.ChunkSize = struct.unpack_from("<I", ChunkHeader, 4)[0]
        self.ChunkSize2 = struct.unpack_from("<I", ChunkHeader, 8)[0]
        self.PaddingSize = struct. unpack_from("<I", ChunkHeader, 12)[0]
        
        f.seek(self.PaddingSize, 1)
        

class ModelTable:
    def __init__(self, f, Header: Chunk):      
        self.Header = Header
        f.seek(24, 1)
        self.ModelNameHash = f.read(4)
        
        f.seek(20, 1)
        self.ModelNameMarker = f.read(4)
        self.ModelName = f.read(36).decode('ascii').strip('\x00')
        
        
        self.Unknown = f.read(96)
        
        self.BonePaletteID = struct.unpack("<I", self.Unknown[88:92])[0]
       
        
        self.Read = f.read(152)
        
        self.MeshCount = self.Read[8]
        
        self.FinalBlockSize = struct.unpack("<I", f.read(4))[0]
        
        f.seek(12, 1)
        
        self.Current_Offsets = []
        self.MeshOffsetsList = []
        
        for i in range(self.MeshCount):
            self.current_offset = f.tell()
            self.Current_Offsets.append(self.current_offset)
            
            self.MeshOffset = struct.unpack("<I", f.read(4))[0]
            self.MeshOffsetsList.append(self.MeshOffset)
            
            f.seek(4, 1)
            
        
        self.NumPrimitivesList = []
        self.MeshPositionsInIndexBuffer = []
        self.MaterialIDs = []
        self.VertexDeclarationIDs = []
        self.IndexBufferIDs = []
        self.Vertex_Buffer0IDs = []
        self.Vertex_Buffer1IDs = []
        self.Vertex_Buffer2IDs = []
        
        
        
        
        
        
        for m in range(self.MeshCount):
            f.seek(self.Current_Offsets[m] + self.MeshOffsetsList[m], 0)
            
            f.seek(24, 1)
            
            self.MaterialID = struct.unpack("<I", f.read(4))[0]
            
            self.MaterialIDs.append(self.MaterialID)
            
            f.seek(28, 1)
            
            self.VertexDeclarationID = struct.unpack("<I", f.read(4))[0]
            
            self.VertexDeclarationIDs.append(self.VertexDeclarationID)
            
            f.seek(28, 1)
            
            self.IndexBufferID = struct.unpack("<I", f.read(4))[0]
            
            self.IndexBufferIDs.append(self.IndexBufferID)
            
            f.seek(28, 1)
            
            self.Vertex_Buffer0ID = struct.unpack("<I", f.read(4))[0]
            
            self.Vertex_Buffer0IDs.append(self.Vertex_Buffer0ID)
            
            f.seek(28, 1)
            
            self.Vertex_Buffer1ID = struct.unpack("<I", f.read(4))[0]
            
            self.Vertex_Buffer1IDs.append(self.Vertex_Buffer1ID)
            
            f.seek(28, 1)
            
            self.Vertex_Buffer2ID = struct.unpack("<I", f.read(4))[0]
            
            self.Vertex_Buffer2IDs.append(self.Vertex_Buffer2ID)
            
            f.seek(40, 1)
            
            self.MeshPositionInIndexBuffer = struct.unpack("<I", f.read(4))[0] # To be multiplied by 2 or 4 to turn into offset relative to start of Index Buffer
            
            self.MeshPositionsInIndexBuffer.append(self.MeshPositionInIndexBuffer)
            
            self.NumPrimitives = struct.unpack("<I", f.read(4))[0] # Triangle Count
            
            self.NumPrimitivesList.append(self.NumPrimitives)
            
            
            f.seek(36, 1)
  
              
class MaterialChunk:
    def __init__(self, f, Header: Chunk):
        self.Header = Header
        f.seek(24, 1)
        self.MaterialNameHash = struct.unpack("<I", f.read(4))[0]
        f.seek(20, 1)
        self.MaterialNameMarker = f.read(4)
        self.MaterialName = f.read(36).decode('ascii').strip('\x00')
        
        f.seek(Header.ChunkSize - Header.PaddingSize - 88, 1)
        
        align_to_16(f)
        
class BonePaletteChunk:
    def __init__(self, f, Header: Chunk):
        self.Header = Header
        f.seek(24, 1)
        self.BonePaletteID = struct.unpack("<I", f.read(4))[0]
        f.seek(20, 1)
        self.BonePaletteNameMarker = f.read(4)
        self.BonePaletteName = f.read(36).decode('ascii').strip('\x00')
        f.seek(4, 1)
        self.BoneCount = struct.unpack("<I", f.read(4))[0]
        
        f.seek(32, 1)
        self.BonePaletteIndices = f.read(160)
        
        self.BoneNames = []
        for i in range(self.BoneCount):
            self.BoneName = f.read(64).decode('ascii').strip('\x00')
            self.BoneNames.append(self.BoneName)
            
        self.BoneIDs = f.read(4 * self.BoneCount * 2) # Repeated Twice

class IndexBuffer:
    def __init__(self, f, Header: Chunk):
        self.Header = Header
        f.seek(16, 1)
        f.seek(Header.PaddingSize, 1)
        f.seek(24, 1)
        self.IndexBufferID = struct.unpack("<I", f.read(4))[0]
        f.seek(20, 1)
        self.IndexBufferNameMarker = f.read(4)
        self.IndexBufferName = f.read(36).decode('ascii').strip('\x00')
        
        f.seek(4, 1)
        self.NumBytes = struct.unpack("<I", f.read(4))[0]
        
        f.seek(8, 1)
        self.IndexStride = struct.unpack("<I", f.read(4))[0]
        self.NumIndices = struct.unpack("<I", f.read(4))[0]
        
        self.Rest_Unknown = f.read(192)
        
        self.Indices = []
        for i in range(self.NumIndices):
            if self.IndexStride == 2:
                Index = struct.unpack("<H", f.read(2))[0]
                self.Indices.append(Index)
                
            elif self.IndexStride == 4:
                Index = struct.unpack("<I", f.read(4))[0]
                self.Indices.append(Index)
                
                
        f.seek(self.Header.ChunkSize - self.NumBytes - 304 - self.Header.PaddingSize, 1)
        
        
class VertexBuffer_0: # Mainly contains Positions
    def __init__(self, f, model_table_info: ModelTable, vertex_declaration_id):

        
        f.seek(16, 1)
        align_to_16(f)
        f.seek(24, 1)
        
        self.Model_Table_Info = model_table_info
        self.VertexDeclarationID = vertex_declaration_id
        self.VertexBuffer_0ID = struct.unpack("<I", f.read(4))[0]
        f.seek(20, 1)
        self.VertexBuffer_0NameMarker = f.read(4)
        self.VertexBuffer_0Name = f.read(36).decode('ascii').strip('\x00')
        
        f.seek(4, 1)
        self.NumBytes = struct.unpack("<I", f.read(4))[0]
        
        f.seek(8, 1)
        self.VertexStride = struct.unpack("<I", f.read(4))[0]
        self.NumVertices = struct.unpack("<I", f.read(4))[0]
        
        self.Rest_Unknown = f.read(192)
        
        self.Positions = []
        self.Normals = []
        self.Tangents = []
        self.UVs0 = []
        self.UVs1 = []
        self.Colors = []
        
        for i in range(self.NumVertices):
            if self.VertexDeclarationID in [661362023, 3795119994, 3213889182, 3499094810]:
                p1 = struct.unpack("<f", f.read(4))[0]
                p2 = struct.unpack("<f", f.read(4))[0]
                p3 = struct.unpack("<f", f.read(4))[0]
                p4 = struct.unpack("<f", f.read(4))[0] 

                n1 = f.read(1)[0] / 127.0
                n2 = f.read(1)[0] / 127.0
                n3 = f.read(1)[0] / 127.0
                n4 = f.read(1)[0] / 127.0

                t1 = f.read(1)[0] / 127.0
                t2 = f.read(1)[0] / 127.0
                t3 = f.read(1)[0] / 127.0
                t4 = f.read(1)[0] / 127.0

                self.Positions.append([p1, p2, p3])
                self.Normals.append([n1, n2, n3])
                self.Tangents.append([t1, t2, t3, t4])


            elif self.VertexDeclarationID in [2434669137, 4067430294, 2611383740]:
                p1 = struct.unpack("<f", f.read(4))[0]
                p2 = struct.unpack("<f", f.read(4))[0]
                p3 = struct.unpack("<f", f.read(4))[0]

             
                self.Positions.append([p1, p2, p3])
               
            
                
        align_to_16(f)
        
        
class VertexBuffer_1: # Mainly contains Positions
    def __init__(self, f, model_table_info: ModelTable, vertex_declaration_id):

    
        f.seek(16, 1)
        align_to_16(f)
        f.seek(24, 1)
        
        self.Model_Table_Info = model_table_info
        self.VertexDeclarationID = vertex_declaration_id
        self.VertexBuffer_1ID = struct.unpack("<I", f.read(4))[0]
        f.seek(20, 1)
        self.VertexBuffer_1NameMarker = f.read(4)
        self.VertexBuffer_1Name = f.read(36).decode('ascii').strip('\x00')
        
        f.seek(4, 1)
        self.NumBytes = struct.unpack("<I", f.read(4))[0]
        
        f.seek(8, 1)
        self.VertexStride = struct.unpack("<I", f.read(4))[0]
        self.NumVertices = struct.unpack("<I", f.read(4))[0]
        
        self.Rest_Unknown = f.read(192)
        
        self.BlendIndicesAndWeights = []
        self.Normals = []
        self.Tangents = []
        self.Colors = []
        self. UVs0 = []
        
        for i in range(self.NumVertices):
            if self.VertexDeclarationID in [661362023, 3795119994, 3213889182, 3499094810]:
                BlendIndex1 = f.read(1)[0]
                BlendIndex2 = f.read(1)[0]
                BlendIndex3 = f.read(1)[0]
                BlendIndex4 = f.read(1)[0]
                
                BlendWeight1 = f.read(1)[0] / 255.0
                BlendWeight2 = f.read(1)[0] / 255.0
                BlendWeight3 = f.read(1)[0] / 255.0
                BlendWeight4 = f.read(1)[0] / 255.0
                
                
                self.BlendIndicesAndWeights.append([(BlendIndex1, BlendWeight1), (BlendIndex2, BlendWeight2), (BlendIndex3, BlendWeight3), (BlendIndex4, BlendWeight4)])
                        
                    
            elif self.VertexDeclarationID == 2434669137:
                U0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                V0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                
                n1 = f.read(1)[0] / 127.0
                n2 = f.read(1)[0] / 127.0
                n3 = f.read(1)[0] / 127.0
                n4 = f.read(1)[0] / 127.0
                
                t1 = f.read(1)[0] / 127.0
                t2 = f.read(1)[0] / 127.0
                t3 = f.read(1)[0] / 127.0
                t4 = f.read(1)[0] / 127.0
                
                R = f.read(1)[0] / 255.0
                G = f.read(1)[0] / 255.0
                B = f.read(1)[0] / 255.0
                A = f.read(1)[0] / 255.0
                
                self.UVs0.append([U0, V0])
                self.Normals.append([n1, n2, n3])
                self.Tangents.append([t1, t2, t3, t4])
                self.Colors.append([R, G, B, A])
                
            
            
            elif self.VertexDeclarationID == 4067430294:
                U0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                V0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                
                n1 = f.read(1)[0] / 127.0
                n2 = f.read(1)[0] / 127.0
                n3 = f.read(1)[0] / 127.0
                n4 = f.read(1)[0] / 127.0
                
                self.UVs0.append([U0, V0])
                self.Normals.append([n1, n2, n3])
                
                
            elif self.VertexDeclarationID == 2611383740:
                U0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                V0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                
                n1 = f.read(1)[0] / 127.0
                n2 = f.read(1)[0] / 127.0
                n3 = f.read(1)[0] / 127.0
                n4 = f.read(1)[0] / 127.0
                
                t1 = f.read(1)[0] / 127.0
                t2 = f.read(1)[0] / 127.0
                t3 = f.read(1)[0] / 127.0
                t4 = f.read(1)[0] / 127.0
                
                self.UVs0.append([U0, V0])
                self.Normals.append([n1, n2, n3])
                self.Tangents.append([t1, t2, t3, t4])

        align_to_16(f)

        
        
        
class VertexBuffer_2: # Mainly contains Positions
    def __init__(self, f, model_table_info: ModelTable, vertex_declaration_id):

        f.seek(16, 1)
        align_to_16(f)
        f.seek(24, 1)
        
        self.Model_Table_Info = model_table_info
        self.VertexDeclarationID = vertex_declaration_id
        self.VertexBuffer_2ID = struct.unpack("<I", f.read(4))[0]
        f.seek(20, 1)
        self.VertexBuffer_2NameMarker = f.read(4)
        self.VertexBuffer_2Name = f.read(36).decode('ascii').strip('\x00')
        
        f.seek(4, 1)
        self.NumBytes = struct.unpack("<I", f.read(4))[0]
        
        f.seek(8, 1)
        self.VertexStride = struct.unpack("<I", f.read(4))[0]
        self.NumVertices = struct.unpack("<I", f.read(4))[0]
        
        self.Rest_Unknown = f.read(192)
        
        self.Positions = []
        self.UVs0 = []
        self.UVs1 = []
        
        for i in range(self.NumVertices):
            if self.VertexDeclarationID in [661362023, 3795119994]:
                U0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                V0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                
                
                self.UVs0.append([U0, V0])
                
            
            elif self.VertexDeclarationID == 3213889182:
                U0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                V0 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                
                U1 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                V1 = np.frombuffer(f.read(2), dtype=np.float16)[0]
                
                f.read(4) # FF FF FF FF
                
                self.UVs0.append([U0, V0])
                self.UVs1.append([U1, V1])
                
     
        align_to_16(f)
        
 
# with open("test.perm.bin", "rb") as f:
#     pattern = b'\xB3\x63\xF9\x6D'

#     data = f.read()
#     pos = data.find(pattern)
    
#     if pos != -1:
#         print(f"Pattern found at offset: {pos}")
#         f.seek(pos, 0)
#         chunk = Chunk(f)
#         Model_Table = ModelTable(f)
#     else:
#         print("Pattern not found")
        
#     file_size = os.path.getsize("test.perm.bin")
    
#     f.seek(0, 0)
#     while f.tell() < file_size:
#         chunk = Chunk(f)
#         print(chunk.ChunkID)
#         print(f.tell())      
        
#         if chunk.ChunkID == 4126691695:
#             Material_Chunk = MaterialChunk(f, chunk)
        
#         elif chunk.ChunkID == 2552518363:
#             Bone_Palette_Chunk = BonePaletteChunk(f)
            
#         elif chunk.ChunkID == 2056721529:
#             read_into = f.read(88)
            
#             if b'Index' in read_into:
#                 f.seek(-88, 1)
#                 Index_Buffer = IndexBuffer(f, chunk)
                
#             elif b'0.0' in read_into:
#                 f.seek(-88, 1)
#                 Vertex_Buffer_0 = VertexBuffer_0(f, Model_Table, chunk)
                
#             elif b'1.0' in read_into:
#                 f.seek(-88, 1)
#                 Vertex_Buffer_1 = VertexBuffer_1(f, Model_Table, chunk)
                
#             elif b'2.0' in read_into:
#                 f.seek(-88, 1)
#                 Vertex_Buffer_2 = VertexBuffer_2(f, Model_Table, chunk)
                
# print(Material_Chunk.MaterialName)
# print(Bone_Palette_Chunk.BonePaletteName)
# print(Index_Buffer.IndexBufferName)

# print(Index_Buffer.NumBytes)
# print(Index_Buffer.IndexStride)
# print(Index_Buffer.NumIndices)
    
# print(Model_Table.MeshCount)

# for i in range(3):
#     print(Model_Table.NumPrimitivesList[i])
    
# print(Vertex_Buffer_0.NumBytes)
# print(Vertex_Buffer_1.NumBytes)
# print(Vertex_Buffer_2.NumBytes)
