import json
import logging
import os
from dotenv import load_dotenv
from openai import OpenAI
from pyfiglet import Figlet
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import convert_to_dict

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
# so that we can access the OpenAI API key
load_dotenv()

# Get the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


def print_ascii_header():
    custom_fig = Figlet(font='slant')
    ascii_art = custom_fig.renderText("OPEN T-DATA SDK")

    border = '+' + '-' * (len(ascii_art.split('\n')[0]) + 2) + '+'

    print(border)
    for line in ascii_art.split('\n'):
        if line.strip():
            print(f"| {line:<{len(border) - 4}} |")
    print(border)

    # Print version and copyright
    version_info = "version: v0.1.2-alpha(I-RC)"
    copyright_info = "copyright @anurag-bit 2024"
    print(f"| {version_info:<{len(border) - 4}} |")
    print(f"| {copyright_info:<{len(border) - 4}} |")
    print(border)
    print()
    input("Press Enter to start data pre-processing...")
    print()


def create_folder_structure(base_dir):
    ingest_dir = os.path.join(base_dir, 'ingest')
    datasheets_dir = os.path.join(ingest_dir, 'datasheets')
    code_ref_dir = os.path.join(ingest_dir, 'C-code-reference')
    output_dir = os.path.join(base_dir, 'output')

    os.makedirs(datasheets_dir, exist_ok=True)
    os.makedirs(code_ref_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    return datasheets_dir, code_ref_dir, output_dir


def find_file(directory, extension):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                return os.path.join(root, file)
    return None


def process_pdf_to_summary(pdf_path, use_openai=False):
    logging.debug("Starting PDF processing")
    elements = partition_pdf(
        filename=pdf_path,
        strategy="hi_res",
        extract_images_in_pdf=True,
        extract_image_block_types=["Image", "Table"],
        extract_image_block_to_payload=False,
        extract_image_block_output_dir="images"
    )
    logging.debug("PDF partitioned")
    processed_data = convert_to_dict(elements)
    logging.debug("Data converted to dict")
    summary = extract_relevant_info(processed_data)
    logging.debug("Relevant info extracted")

    if use_openai:
        logging.debug("Enhancing summary with GPT-4")
        summary = enhance_with_gpt4(summary)
        logging.debug("Summary enhanced with GPT-4")

    return summary


def extract_relevant_info(data):
    relevant_info = {
        "device_name": "",
        "registers": [],
        "memory_map": [],
        "interrupts": [],
        "power_management": [],
        "interfaces": [],
        "pin_configuration": [],
        "timing_diagrams": [],
        "electrical_characteristics": [],
        "operating_conditions": [],
        "package_information": [],
        "application_circuits": [],
        "boot_sequence": [],
        "initialization_code": [],
        "driver_api": [],
        "error_handling": [],
        "security_features": [],
        "debugging_features": [],
        "performance_metrics": [],
        "compatibility_information": [],
        "firmware_updates": [],
        "power_consumption": [],
        "thermal_management": [],
        "supported_protocols": [],
        "example_usage": [],
        "documentation_references": [],
        "communication_protocols": [],
        "hardware_interfaces": [],
        "memory_management": [],
        "power_modes": [],
        "clock_configuration": [],
        "reset_procedures": [],
        "diagnostic_features": [],
        "safety_features": [],
        "compliance_standards": [],
        "environmental_conditions": [],
        "lifecycle_management": [],
        "testing_procedures": [],
        "troubleshooting_guides": [],
        "performance_benchmarks": [],
        "optimization_tips": [],
        "known_issues": [],
        "workarounds": [],
        "release_notes": [],
        "change_log": []
    }

    for element in data:
        text = element.get("text", "").lower()
        if "device name" in text:
            relevant_info["device_name"] = text
        elif "register" in text:
            relevant_info["registers"].append(text)
        elif "memory map" in text:
            relevant_info["memory_map"].append(text)
        elif "interrupt" in text:
            relevant_info["interrupts"].append(text)
        elif "power management" in text:
            relevant_info["power_management"].append(text)
        elif "interface" in text:
            relevant_info["interfaces"].append(text)
        elif "pin configuration" in text:
            relevant_info["pin_configuration"].append(text)
        elif "timing diagram" in text:
            relevant_info["timing_diagrams"].append(text)
        elif "electrical characteristic" in text:
            relevant_info["electrical_characteristics"].append(text)
        elif "operating condition" in text:
            relevant_info["operating_conditions"].append(text)
        elif "package information" in text:
            relevant_info["package_information"].append(text)
        elif "application circuit" in text:
            relevant_info["application_circuits"].append(text)
        elif "boot sequence" in text:
            relevant_info["boot_sequence"].append(text)
        elif "initialization code" in text:
            relevant_info["initialization_code"].append(text)
        elif "driver api" in text:
            relevant_info["driver_api"].append(text)
        elif "error handling" in text:
            relevant_info["error_handling"].append(text)
        elif "security feature" in text:
            relevant_info["security_features"].append(text)
        elif "debugging feature" in text:
            relevant_info["debugging_features"].append(text)
        elif "performance metric" in text:
            relevant_info["performance_metrics"].append(text)
        elif "compatibility information" in text:
            relevant_info["compatibility_information"].append(text)
        elif "firmware update" in text:
            relevant_info["firmware_updates"].append(text)
        elif "power consumption" in text:
            relevant_info["power_consumption"].append(text)
        elif "thermal management" in text:
            relevant_info["thermal_management"].append(text)
        elif "supported protocol" in text:
            relevant_info["supported_protocols"].append(text)
        elif "example usage" in text:
            relevant_info["example_usage"].append(text)
        elif "documentation reference" in text:
            relevant_info["documentation_references"].append(text)
        elif "communication protocol" in text:
            relevant_info["communication_protocols"].append(text)
        elif "hardware interface" in text:
            relevant_info["hardware_interfaces"].append(text)
        elif "memory management" in text:
            relevant_info["memory_management"].append(text)
        elif "power mode" in text:
            relevant_info["power_modes"].append(text)
        elif "clock configuration" in text:
            relevant_info["clock_configuration"].append(text)
        elif "reset procedure" in text:
            relevant_info["reset_procedures"].append(text)
        elif "diagnostic feature" in text:
            relevant_info["diagnostic_features"].append(text)
        elif "safety feature" in text:
            relevant_info["safety_features"].append(text)
        elif "compliance standard" in text:
            relevant_info["compliance_standards"].append(text)
        elif "environmental condition" in text:
            relevant_info["environmental_conditions"].append(text)
        elif "lifecycle management" in text:
            relevant_info["lifecycle_management"].append(text)
        elif "testing procedure" in text:
            relevant_info["testing_procedures"].append(text)
        elif "troubleshooting guide" in text:
            relevant_info["troubleshooting_guides"].append(text)
        elif "performance benchmark" in text:
            relevant_info["performance_benchmarks"].append(text)
        elif "optimization tip" in text:
            relevant_info["optimization_tips"].append(text)
        elif "known issue" in text:
            relevant_info["known_issues"].append(text)
        elif "workaround" in text:
            relevant_info["workarounds"].append(text)
        elif "release note" in text:
            relevant_info["release_notes"].append(text)
        elif "change log" in text:
            relevant_info["change_log"].append(text)

    return relevant_info


def enhance_with_gpt4(summary):
    prompt = [
        {
            "role": "system",
            "content": "You are an expert in computational analysis and technical hardware and its documentation."
        },
        {
            "role": "user",
            "content": """
You are an expert in analyzing JSON summary related to Linux device drivers. Given the following summary extracted from a PDF, provide additional relevant information and improve the summary with more detailed insights. I'm giving you JSON-based context data on a sensor or microdevice. I want a concise practical summary on it like this:

Example:
Device Name: AIS328DQ
Device Type: 3-axis linear accelerometer
Key Features:
- AEC-Q100 qualification
- Wide supply voltage range: 2.4 V to 3.6 V
- Low voltage compatible IOs: 1.8 V
- Ultra-low-power mode consumption: down to 10 μA
- ±2g/±4g/±8g dynamically selectable full scale
- SPI / I²C digital output interface
- 16-bit data output
- 2 independent programmable interrupt generators
- Extended temperature range: -40 °C to 105 °C
- Embedded self-test
- High shock survivability: up to 10000 g
- ECOPACK, RoHS and "Green" compliant

Communication Interface: SPI / I²C digital output interface

Register Addresses and Descriptions:
- 0Fh WHO_AM_I: Device identification register
- 20h CTRL_REG1: Power mode selection and data rate selection
- 21h CTRL_REG2: High-pass filter mode selection and cut-off frequency configuration
- 22h CTRL_REG3: Configuration for interrupt 1 source
- 23h CTRL_REG4: Block data update, big/little endian data selection, full-scale selection, self-test enable, SPI serial interface mode selection
- 24h CTRL_REG5: Turn-on mode selection for sleep-to-wake function
- 25h HP_FILTER_RESET: Dummy register for resetting the high-pass filter
- 26h REFERENCE: Reference value for high-pass filter
- 27h STATUS_REG: Status of overrun and new data available for X, Y, and Z axes
- 28h, 29h OUT_X_L, OUT_X_H: X-axis acceleration data
- 2A, 2B, 2C, 2D OUT_Y_L, OUT_Y_H, OUT_Z_L, OUT_Z_H: Y-axis and Z-axis acceleration data
- 30h INT1_CFG: Configuration for interrupt 1 source
- 31h INT1_SRC: Interrupt 1 source register
- 32h INT1_THS: Interrupt 1 threshold
- 33h INT1_DURATION: Minimum duration of interrupt 1 event to be recognized
- 34h INT2_CFG: Configuration for interrupt 2 source
- 35h INT2_SRC: Interrupt 2 source register
- 36h INT2_THS: Interrupt 2 threshold
- 37h INT2_DURATION: Minimum duration of interrupt 2 event to be recognized

Package Information: QFN 24 (4 x 4 x 1.8 mm)
Soldering Information:
- Compliant with JEDEC J-STD-020C, in MSL3 conditions
- General guidelines and recommendations for PCB design, stencil design, and solder paste application
- Process considerations for soldering and cleaning

Here is the real raw data that you have to generate summary from. Note: only take inspiration from the above example, generate using the raw data. Also, do not use any formatting like bold or italics. It should have all details about the device hardware and types and properties.

Raw data Summary:
"""
        },
        {
            "role": "user",
            "content": summary
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=prompt,
        max_tokens=4096
    )

    enhanced_summary = response.choices[0].message.content.strip()
    try:
        return json.loads(enhanced_summary)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON: {e}")
        return enhanced_summary


def generate_context_from_files(datasheets_dir, code_ref_dir, output_dir):
    # Read C file
    c_file_path = find_file(code_ref_dir, ".c")
    if not c_file_path:
        logging.error("No C file found")
        return

    with open(c_file_path, "r", encoding="utf-8") as file:
        fns_text = file.read()

    # Read summary JSON
    summary_file_path = os.path.join(datasheets_dir, "summary.json")
    if not os.path.exists(summary_file_path):
        logging.error("Summary JSON file not found")
        return

    with open(summary_file_path, "r", encoding="utf-8") as file:
        ex_fn_text = file.read()

    # Define the prompts
    prompts = [
        {
            "role": "system",
            "content": "You are an expert C and C++ programmer."
        },
        {
            "role": "user",
            "content": """I'm giving you a hardware datasheet summary generated using unstructured.io, along with its related hardware code. Using this data, you have to generate all essential functions that are used to inialiase, powerUP powerDown and start, stop,and perform certain actions, This is supposed to really detailed training data for an AI, I want you to generate a comprehensive JSON output with the following requirements:

 Task_name: A one line detailed description of what that function does, with it's context of entire purpose of the entire file

 Instruction: In a question or task oriented tone, write a action statement of the code.

 Information:breifly explain what the function does, in context of the hardware, the module and the function, the concerned module performs on the software.

 Solution: the function code

 Remember you have to perform this for each and every function required!


follow this template strictly

    TEMPLATE:
            {
    "message":[
        {
        "role":"user",
        "TaskName":"",
        "Instruction":"",
        "Information":"",

        },
        {
            "role":"assistant",
            "content":{
                "text":"The driver code will contain all these parts in order -",
               "Solution":""
            }


        }
    ]
}


Now here is a reference only sample of how this has to be done, remember this is just a reference, you have to generate the code using the raw data provided next.
now assume you have some python code that you want to generate this kind of JSON output for, you can use the following code as a reference to generate the JSON output:
     Example Raw code:
    #!/usr/bin/env python # -*- coding: utf-8 -*-
    '''Simple server which adds a DocumentWordsProvider to the CodeCompletion worker.
    On Windows, this script is frozen by freeze_setup.py (cx_Freeze).'''

    from pyciode.core import backend
    if name -- backend.CodeCompletionWorker.providers.append(backend.DocumentWordsProvider())
    backend.serve_forever()



 Example reference Generation :

 "message":[
     {
     "role":"user",
     "TaskName":" Adding a DocumentWordsProvider to a CodeCompletion worker ",
     "Instruction":"Write a Python code to add a DocumentWordsProvider to a CodeCompletion worker.",
     "Information":"The CodeCompletion worker is from the pyciode.core.backend module. The DocumentWordsProvider is used to provide word completion suggestions for a given document. ",

     },
     {
         "role":"assistant",
         "content":{
             "text":"The driver code will contain all these parts in order -",
            "Solution":from pyciode.core import backend
           if name_ == '_main_': backend.CodeCompletionWorker.providers.append(backend.DocumentWordsProvider()) backend.serve_forever() Note: This script is used to add a DocumentWordsProvider to a CodeCompletion worker in a simple server. The script is frozen by freeze_setup.py on Windows.
         }


     }
 ]







 """
        },
        {
            "role": "user",
            "content": fns_text
        },
        {
            "role": "assistant",
            "content": ex_fn_text
        },

    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=prompts,
        max_tokens=4096  # Set the maximum number of tokens to generate, limit for GPT-4 is 8096
    )
    generated_code = response.choices[0].message.content.strip()

    output_file_path = os.path.join(output_dir, "generated_driver_code.json")
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(generated_code)

    logging.info(f"Generated code written to {output_file_path}")


# Main function
def main(base_dir):
    datasheets_dir, code_ref_dir, output_dir = create_folder_structure(base_dir)

    pdf_path = find_file(datasheets_dir, ".pdf")
    if pdf_path:
        summary = process_pdf_to_summary(pdf_path, use_openai=False)
        summary_file_path = os.path.join(datasheets_dir, "summary.json")
        with open(summary_file_path, "w", encoding="utf-8") as file:
            json.dump(summary, file, indent=4)
        logging.info(f"Summary written to {summary_file_path}")

    generate_context_from_files(datasheets_dir, code_ref_dir, output_dir)



if __name__ == "__main__":
    print_ascii_header()
    base_dir = os.getcwd()
    main(base_dir)
