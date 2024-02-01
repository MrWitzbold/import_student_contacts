import re

def contains_alphabetic_letters(input_string):
    return any(char.isalpha() for char in input_string)

def filter_lines_from_html(html_code):
    result_lines = []
    lines = html_code.split('\n')
    for line in lines:
        if re.search(r'\(51\)|Nome:', line):
            result_lines.append(line.strip())
    result_string = '\n'.join(result_lines)
    return result_string
    
def extract_content(html_string):
    # Remove lines that don't contain "Nome: " or (51)
    lines = html_string.split('\n')
    filtered_lines = [line for line in lines if "Nome: " in line or "(51)" in line]
    filtered_html = '\n'.join(filtered_lines)

    # Use regular expression to find content between '>' and '<'
    pattern = re.compile(r'<span[^>]*>(.*?)</span>', re.DOTALL)
    matches = pattern.findall(filtered_html)

    # Join the extracted content into a comma-separated string
    result_string = ', '.join(matches)
    
    return result_string

def generate_vcf(students):
    vcf_content = ""

    for student_id, student_info in students.items():
        for phone_number in student_info['phone_numbers']:
            vcf_content += "\nBEGIN:VCARD"
            vcf_content += "\nVERSION:3.0"
            vcf_content += "\nFN:" + student_info['name']
            vcf_content += "\nTEL;TYPE=CELL:" + phone_number
            vcf_content += "\nCATEGORIES:myContacts"
            vcf_content += "\nEND:VCARD\n"


    return vcf_content

html_code = ''' # Get .html file from telefones in estudantes matriculados

'''

output_string = filter_lines_from_html(html_code)
contacts = str(extract_content(output_string)).replace("Nome: ", "").replace(", ,", ",").replace("(51) ", "51").replace(", ", ",").replace("()", "")[1:]

students = {}
student_count = 0
# Function to add a student
def add_student(student_id, name, phone_numbers=None):
    students[student_id] = {'name': name, 'phone_numbers': phone_numbers or []}

contact_list = contacts.split(",")
for i in range(0, len(contact_list)):
    if contains_alphabetic_letters(contact_list[i]):
        numbers = []
        j = i+1
        if j <= len(contact_list):
            while contains_alphabetic_letters(contact_list[j]) == False:
                numbers.append(contact_list[j])
                if j < len(contact_list)-1:
                    j += 1
                else:
                    break
        add_student(student_count, contact_list[i], numbers)
        student_count += 1
        
print(generate_vcf(students))
