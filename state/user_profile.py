

class UserProfile:
    def __init__(self, company_name: str = '', topic: str = '', timeframe: str = ''):
        self.company_name = company_name
        self.topic = topic
        self.timeframe = timeframe
        
    def check_preferences(self)-> list:
        missing_fields = []
        if self.company_name == '':
            missing_fields.append("company name")
        if self.topic == '':
            missing_fields.append("topic")
        if self.timeframe == '':
            missing_fields.append("timeframe")
            
        return missing_fields
    
    def missing_preferences(self):
        missing_fields = self.check_preferences()
        return f"your missing fields: {', '.join(missing_fields)}. Please add them." if missing_fields else "All preferences are set."