"""
Author: Ali Gholami
"""
import sys, os, string, getopt

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'analyzer.py -i <inputfile> -o <outputfile>'
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print 'analyzer.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg   

   if os.path.isfile(inputfile):
     infile = open(inputfile)
     outfile = open(outputfile, 'w')
     kernel_usage(infile, outfile)
     infile.close()
     outfile.close()
   else:
     print "File: ", inputfile, " does not exist!"
     sys.exit(2)

"""
This function generates the lines that are used used 
by each source file in the kernel
"""
def kernel_usage(infile, outfile):

    for lines in infile:
      if "SF:" in lines:
        outfile.write(lines)

      if ("DA:" in lines) and ("FNDA" not in lines):
        lines = lines.replace("DA:", "")
        line = lines.split(",")
        outfile.write(line[0]+'\n')

      if "end_of_record" in lines:
        outfile.write('\n')   

    pass

if __name__ == "__main__":
   main(sys.argv[1:])
