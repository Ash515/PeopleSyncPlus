import xml.etree.ElementTree as ET
import datetime

def generate_license(company_name, admin_email, max_users, features, valid_days=365):
    """Generates an XML license file."""
    license_data = ET.Element("License")

    ET.SubElement(license_data, "LicenseKey").text = "ABC123-XYZ789-PQR456"
    ET.SubElement(license_data, "CompanyName").text = company_name
    ET.SubElement(license_data, "AdminEmail").text = admin_email
    
    valid_from = datetime.datetime.now().strftime("%Y-%m-%d")
    valid_to = (datetime.datetime.now() + datetime.timedelta(days=valid_days)).strftime("%Y-%m-%d")
    
    ET.SubElement(license_data, "ValidFrom").text = valid_from
    ET.SubElement(license_data, "ValidTo").text = valid_to
    ET.SubElement(license_data, "MaxUsers").text = str(max_users)
    
    features_element = ET.SubElement(license_data, "Features")
    for feature in features:
        ET.SubElement(features_element, "Feature", name=feature).text = "Enabled"

    tree = ET.ElementTree(license_data)
    tree.write("license.xml")
    print("License file generated: license.xml")

# Example usage:
generate_license("Example Corp", "admin@example.com", 50, ["UserManagement", "Reports", "Security"])
