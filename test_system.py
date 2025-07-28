#!/usr/bin/env python3
"""
Test script for the EOTSS Hosting Recommendation System
This script tests the email automation and review system functionality.
"""

import json
import os
import uuid
from datetime import datetime

def create_test_assessment():
    """Create a test assessment for testing purposes."""
    
    # Test agency info
    agency_info = {
        'agency_name': 'Test Agency',
        'contact_name': 'John Doe',
        'contact_email': 'test@example.com',
        'department': 'IT Department'
    }
    
    # Test assessment data
    assessment_data = {
        'recommendation': 'AWS',
        'scores': 'AWS: 15\nOn Prem Cloud: 8\nPhysical: 4',
        'explanations': 'High fault tolerance needs are best met by AWS.\nLow budget sensitivity favors AWS cost efficiency.\nModern, cloud-ready applications are ideal for AWS.',
        'answers': 'Fault Tolerance (Low/Moderate/High): High\nLatency Sensitivity (Low/Moderate/High): Low\nData Volume (Low/Moderate/High): Low\nSecurity Needs (Low/Moderate/High): Low\nMigration Complexity (Low/Moderate/High): Low\nOperational Expertise (aws/vmware/minimal): aws\nBudget Sensitivity (Low/Moderate/High): Low\nDoes your application have specific compliance requirements (yes/no)?: no\nDo you expect rapid growth or fluctuating workloads (yes/no)?: yes\nApplication Age (determined): Modern\nIs the app containerized or able to be containerized (e.g., Docker)?: yes\nDoes the app run on a cloud-supported OS/runtime (e.g., modern Linux, Windows Server 2016+)?: yes\nDoes the app avoid relying on physical hardware or specialized networking?: yes'
    }
    
    # Create assessment record
    assessment_id = str(uuid.uuid4())
    assessment_record = {
        "id": assessment_id,
        "status": "pending",
        "submitted_at": datetime.now().isoformat(),
        "agency_info": agency_info,
        "assessment_data": assessment_data
    }
    
    # Save to file
    data_dir = 'assessment_data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    assessment_file = os.path.join(data_dir, f"{assessment_id}.json")
    with open(assessment_file, 'w') as f:
        json.dump(assessment_record, f, indent=2)
    
    print(f"✅ Test assessment created with ID: {assessment_id}")
    print(f"📁 Saved to: {assessment_file}")
    print(f"🔗 Review URL: http://localhost:5000/review/{assessment_id}")
    print(f"📊 Dashboard URL: http://localhost:5000/dashboard")
    
    return assessment_id

def test_file_structure():
    """Test that the file structure is correct."""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/form.html',
        'templates/result.html',
        'templates/review.html',
        'templates/dashboard.html'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
    
    # Check if assessment_data directory exists
    if os.path.exists('assessment_data'):
        print("✅ assessment_data/ directory exists")
    else:
        print("⚠️  assessment_data/ directory will be created when needed")

def main():
    """Main test function."""
    print("🧪 EOTSS Hosting Recommendation System - Test Script")
    print("=" * 60)
    
    # Test file structure
    test_file_structure()
    
    # Create test assessment
    print("\n📝 Creating test assessment...")
    assessment_id = create_test_assessment()
    
    print("\n🎯 Test Summary:")
    print(f"• Test assessment ID: {assessment_id}")
    print(f"• Agency: Test Agency")
    print(f"• Recommendation: AWS")
    print(f"• Status: Pending Review")
    
    print("\n🚀 Next Steps:")
    print("1. Start the Flask app: python app.py")
    print("2. Visit: http://localhost:5000/dashboard")
    print("3. Click 'Review' on the test assessment")
    print("4. Test approve/reject functionality")
    print("5. Check email notifications (if configured)")
    
    print("\n📧 Email Testing:")
    print("• Update email credentials in app.py")
    print("• Submit a real assessment through the web form")
    print("• Check that EOTSS receives notification email")
    print("• Test the review link in the email")
    print("• Verify agency receives confirmation email")

if __name__ == "__main__":
    main() 