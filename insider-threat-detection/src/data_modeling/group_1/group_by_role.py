import pandas as pd

# Read the output_final.csv file
output_final = pd.read_csv("output_final.csv")

# Dictionary of selected variables for each role
selected_variables = {
    "Electrical Engineer": ["numlogoffNight", "numPClogoffNight", "numOpenOnPCNight", "numAttachmentNight", "numSendNight", "numEmailSentwithAttachNight", "numPClogonDay", "numOpenOnPCDay", "numAttachmentDay", "numSendDay", "numEmailSentwithAttachDay"],
    "IT Admin": ["numlogoffNight", "onoffNotsameDay", "numConnectionDay", "numCopyFromDeviceNight", "numWriteFromDeviceNight", "numWebAccNight", "numDownloadNight", "numPClogoffNight", "numPCwithUSBDay", "numCopy2DeviceNight", "numCopyFromDeviceNight", "numWebAccDay", "numURLAccessedNight"],
    "Salesman": ["numlogonDay", "numPClogonDay", "onoffNotsameNight", "numConnectionNight", "numWriteFromDeviceNight", "numUploadNight", "numSendDay", "numlogonNight", "onoffNotsameDay", "numPCwithUSBNight", "numWrite2DeviceDay", "numOpenOnPCDay", "numAttachmentDay", "numReceiveDay"]
}

# Iterate over each role and its corresponding selected variables
for role, vars in selected_variables.items():
    # List of indices of selected variables
    selected_indices = [output_final.columns.get_loc(var) for var in vars]

    # Filter the rows based on the role column
    output_final_role = output_final.loc[output_final["role"] == role]

    # Select the columns based on the indices of selected variables
    output_final_role = output_final_role.iloc[:, selected_indices]

    # Write the output csv file for each role
    output_final_role.to_csv(f"output_final_{role}.csv", index=False)
