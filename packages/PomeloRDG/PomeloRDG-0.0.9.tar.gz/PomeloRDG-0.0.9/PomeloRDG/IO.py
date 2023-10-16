import os
import PomeloRDG.Utils as Utils

class IO():
    def __init__(self, filename, id = None, insuffix = ".in", outsuffix = ".out"):
        self.filename = filename
        self.id = id if id != None else ""
        self.insuffix = insuffix
        self.outsuffix = outsuffix
        self.infile = open(str(self.filename) + str(self.id) + str(self.insuffix), "w")
        self.outfile = open(str(self.filename) + str(self.id) + str(self.outsuffix), "w")
        
    def __getdata__(self, *args):
        """
        Get the data of args.
        """
        
        data = []
        for val in args:
            if Utils.list_like(val):
                for val_elm in val:
                    self.__getdata__(val_elm, data = data)
            else:
                data.append(val)
        return data
        
    def input_write(self, *args, sep = " ", end = "\n"):
        """
        Write data to the input file.
        """
        
        data = self.__getdata__(*args)
        for val in data:
            self.infile.write(str(val) + sep)
        self.infile.write(end)
        
    def output_write(self, *args, sep = " ", end = "\n"):
        """
        Write data to the output file.
        """
        
        data = self.__getdata__(*args)
        for val in data:
            self.outfile.write(str(val) + sep)
        self.outfile.write(end)
        
    def output_gen(self, cppfile):
        """
        Generate standard answers by using the C++.
        
        C++ code template:

        int main(int argc, char* argv[]){
            char infile[110], outfile[110];
            strcpy(infile, argv[1]), strcpy(outfile, argv[2]);
            freopen(infile, "r", stdin), freopen(outfile, "w", stdout);
            // Your Code
            return 0;
        }
        """
        
        open(str(self.filename) + str(self.id) + str(self.insuffix), "w")
        os.system("g++ -Ofast -std=c++14 {}".format(cppfile))
        os.system("./a.out {}{}.in {}{}.out".format(self.filename, str(self.id), self.filename, str(self.id)))
        os.remove("./a.out")