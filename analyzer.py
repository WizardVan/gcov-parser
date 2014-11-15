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
     infile = open(inputfile, 'r')
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
    
    tmp_path= ""

    "A set of lines used in the SF"
    da_values = set()    
    usage_dict = {}    

    for lines in infile:
      if "SF:" in lines:
        tmp_path= lines.rstrip(os.linesep)
      
      if ("DA:" in lines) and ("FNDA" not in lines):
        lines = lines.replace("DA:", "")
        line = lines.split(",")
        da_values.add(int(line[0]))

      if "end_of_record" in lines:
        tmp_set = usage_dict.get(tmp_path)
        if tmp_set is not None:
          union = set().union(da_values,tmp_set)
          usage_dict[tmp_path] = sorted(union)
        else:
          usage_dict[tmp_path]= sorted(da_values)
        da_values.clear()

    for sf,da in usage_dict.iteritems():
      outfile.write(sf+'\n')
      da_sorted = sorted(da)
      for lines in da_sorted:
        outfile.write('%d\n'%lines)
        
      outfile.write('\n')
    
    pass


if __name__ == "__main__":
   main(sys.argv[1:])
