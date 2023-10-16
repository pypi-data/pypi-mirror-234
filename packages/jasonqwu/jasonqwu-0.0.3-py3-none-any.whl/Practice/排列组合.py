count = 0
for i in range(1, 5):
    for j in range(1, 5):
        for k in range(1, 5):
            count += 1
            print(f"{i}{j}{k}", end=' ')
print(f"\ncount = {count}")
count = 0
for i in range(1, 5):
    for j in range(1, 5):
        if i != j:
            for k in range(1, 5):
                if i != k and j != k:
                    count += 1
                    print(f"{i}{j}{k}", end=' ')
print(f"\ncount = {count}")
