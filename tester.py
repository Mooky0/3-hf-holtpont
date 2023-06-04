import tests
import main

count = 0
all = 0
passed = []
for idx, i in enumerate(tests.inputs):
    out = main.main(i)
    all += 1
    if (out.strip() == tests.outputs[idx].strip()):
        print("Test " + str(idx+1) + " passed")
        count += 1
        passed.append(idx+1)
    else:
        print("Test " + str(idx+1) + " failed")
        print("Expected:" + tests.outputs[idx] + "\nActual:" + out)
        print("for input: " + i + "\n\n")

print(str(count) + "/" + str(all))
#print(passed)