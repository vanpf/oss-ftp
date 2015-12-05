from oss_file_operation import *

class OssFsImpl:
   

    def __init__(self, bucket_name, endpoint, access_id, access_key):
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.access_id = access_id
        self.access_key = access_key

        self.bucket = oss2.Bucket(oss2.Auth(self.access_id, self.access_key), self.endpoint, self.bucket_name)
        
    def isBucket(self, path):
        phyPath = self.stripLastDelimiter(path)
        index = phyPath.rfind('/')
        if index == 0 and not self.isRoot(path):
            return True
        return False
    
    def isRoot(self, path):
        return path == '/'

    def stripLastDelimiter(self, path):
        if path.endswith('/'):
            path = path[:-1]
        return path

    def getOSSBucketName(self, path):
        if self.isRoot(path):
            return "/"
        phyPath = self.stripLastDelimiter(path)
        index = phyPath.find('/', 1)
        if index <= 0:
            return phyPath[1:]
        else:
            return phyPath[1:index]
        
    def getFileName(self, path):
        if self.isBucket(path):
            return ""
        if path == '/':
            return '/'
        bucket = self.getOSSBucketName(path)
        return path[len(bucket)+2:]
    
    def getParentPhysicalName(self, path):
        if path == '/':
            return '/'

        parentPath = self.stripLastDelimiter(path)

        index = parentPath.rfind('/')
        if index != -1:
            parentPath = parentPath[:index]

        return parentPath

    def normalizeSeparateChar(self, path):
        normalizedPathName = path.replace('\\', '/')
        return normalizedPathName
    
    def getPhysicalName(self, rootDir, curDir, fileName):
        normalizedRootDir = self.normalizeSeparateChar(rootDir)
        if normalizedRootDir[-1] != '/':
            normalizedRootDir += '/'
        normalizedFileName = self.normalizeSeparateChar(fileName)
        normalizedCurDir = curDir
        if normalizedFileName[0] != '/':
            if normalizedCurDir == None:
                normalizedCurDir = '/'
            if normalizedCurDir == '':
                normalizedCurDir = '/'
            normalizedCurDir = self.normalizeSeparateChar(normalizedCurDir)
            if normalizedCurDir[0] != '/':
                normalizedCurDir = '/' + normalizedCurDir
            if normalizedCurDir[-1] != '/':
                normalizedCurDir = normalizedCurDir + '/'
            resArg = normalizedRootDir + normalizedCurDir[1:]
        else:
            resArg = normalizedRootDir

        resArg = self.stripLastDelimiter(resArg)

        st = normalizedFileName.split('/')
        for tok in st:
            if tok == '':
                continue
            if tok == '.':
                continue
            if tok == '..':
                if resArg.startswith(normalizedRootDir):
                    slashIndex = resArg.rfind('/')
                    if slashIndex != -1:
                        resArg = resArg[0:slashIndex]
                continue
            if tok == '~':
                resArg = normalizedRootDir[:-1]
                continue

            resArg = resArg + '/' + tok

        if len(resArg) + 1 == len(normalizedRootDir):
            resArg = resArg + '/'

        return resArg
   
    def get_bucket(self, path):
        path = self.normalizeSeparateChar(path)
        bucket_name = self.getOSSBucketName(path)
        bucket = oss2.Bucket(oss2.Auth(self.access_id, self.access_key), self.endpoint, bucket_name)
        return bucket
    
    def get_object(self, path):
        path = self.normalizeSeparateChar(path)
        object = self.getFileName(path)
        return object

    def open_read(self, path):
        return OssFileOperation(self.get_bucket(path), self.get_object(path)).open_read()
    
    def open_write(self, path):
        return OssFileOperation(self.get_bucket(path), self.get_object(path))
    
    def mkdir(self, path):
        return OssFileOperation(self.get_bucket(path), self.get_object(path)).mkdir()
        
    def listdir(self, path):
        return OssFileOperation(self.get_bucket(path), self.get_object(path)).listdir()
    
    def rmdir(self, path):
        return OssFileOperation(self.get_bucket(path), self.get_object(path)).rmdir()
    
    def remove(self, path):
        return OssFileOperation(self.get_bucket(path), self.get_object(path)).remove()
    
    def rename(self, path1, path2):
        pass
    
    def getsize(self, path):
        return OssFileOperation(self.get_bucket(path), self.get_object(path)).getsize()
    ##not implement
    def getmodify(self, path):
        return OssFileOperation(self.get_bucket(path), self.get_object(path)).getmodify()
    
    def isfile(self, path):
        return OssFileOperation(self.get_bucket(path), self.get_object(path)).isfile()
    
    def isdir(self, path):
        path = self.normalizeSeparateChar(path)
        if self.isBucket(path):
            return True
        if self.isRoot(path):
            return True
        return OssFileOperation(self.get_bucket(path), self.get_object(path)).isdir()
