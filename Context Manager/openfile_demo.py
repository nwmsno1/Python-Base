class OpenFileDemo(object):
    def __init__(self, filename):
        self.filename = filename
 
    def __enter__(self):
        self.f = open(self.filename, 'a+')
        return self.f
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
 
with OpenFileDemo('test.txt') as f:
    f.write('Foo\n')
