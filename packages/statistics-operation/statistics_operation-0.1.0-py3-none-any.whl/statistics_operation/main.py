import operations
import time


input_list = list(map(int, input("Enter the list : ").split(" ")))
print("Mean : ", operations.mean(input_list))
print("Mode : ", operations.mode(input_list))
print("Median : ", operations.median(input_list))
print("Standard deviation : ", operations.standard_devaition(input_list))
print("Variance : ", operations.variance(input_list))
n_input = int(input("Enter the nxn : "))
input_list_1 = []
for i in range(n_input):
    input_list = list(map(int, input("Enter the list : ").split(" ")))
    input_list_1.append(input_list)
print("2-d array : ", input_list_1)
print("Determinant : ", operations.determinant(input_list_1))
print("Inversion : ", operations.transpose(input_list_1))
file_path = input("Enter the file path : ")
with open(file=file_path, mode="w") as file:
    file.write(
        f"Mean : {operations.mean(input_list)}\n"
        f"Mode : {operations.mode(input_list)}\n"
        f"Median : {operations.median(input_list)}\n"
        f"Standard deviation : {operations.standard_devaition(input_list)}\n"
        f"Variance : {operations.variance(input_list)}\n"
        f"Determinant : {operations.determinant(input_list_1)}\n"
        f"Inversion : {operations.transpose(input_list_1)}"
    )
time.sleep(6)
