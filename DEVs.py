import os
import sys
import traceback

def main(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        i = 0
        dev_tags = {"1": "DEV0001", "2": "DEV0002", "3": "DEV0003", "4": "DEV0004", "5": "DEV0005"}
        """
        try:
            exceptions = sys.argv[2]
            
        except IndexError:
            exceptions = ""
        """
        
        exceptions = ""
            
        while i < len(lines):
            for dev_tag in dev_tags:
                if dev_tags[dev_tag] in lines[i] and dev_tag not in exceptions:
                    print("\n" + "=" * 25 + dev_tags[dev_tag] + " line " + str(i + 1) + "=" * 25 + "\n")
                    print(lines[i - 5].replace("\n", ""))
                    print(lines[i - 4].replace("\n", ""))
                    print(lines[i - 3].replace("\n", ""))
                    print(lines[i - 2].replace("\n", ""))
                    print(lines[i - 1].replace("\n", ""))
                    print(lines[i].replace("\n", ""))
                    try:
                        print(lines[i + 1].replace("\n", ""))
                        print(lines[i + 2].replace("\n", ""))
                        print(lines[i + 3].replace("\n", ""))
                        print(lines[i + 4].replace("\n", ""))
                        print(lines[i + 5].replace("\n", ""))
                        
                    except IndexError:
                        pass
                
            i += 1
            
        return 0
    
    except BaseException as e:
        traceback.print_exc()
        print(e)
        sys.exit(1)
            
if __name__ == '__main__':
    try:
        if os.path.isfile(sys.argv[1].replace("\n", "")):
            sys.exit(main(sys.argv[1].replace("\n", "")))
            
        else:
            print("USAGE: {0} <file> <optional-dev-tag-to-hide>".format(sys.argv[0].replace("\n", "")))
            sys.exit(2)
            
    except Exception as e:
        print(e)
        print("USAGE: {0} <file> <optional-dev-tag-to-hide>".format(sys.argv[0].replace("\n", "")))
        sys.exit(3)