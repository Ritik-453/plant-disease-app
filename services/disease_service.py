class DiseaseService:
    def __init__(self):
        # 🌍 Geo mapping
        self.region_map = {
            "Rajasthan": ["Diseased"],
            "Maharashtra": ["Healthy", "Diseased"]
        }

        # 🧾 Treatment mapping
        self.treatment_map = {
            "Healthy": [
                "No treatment needed",
                "Maintain proper watering",
                "Ensure sunlight exposure"
            ],
            "Diseased": [
                "Remove infected leaves",
                "Apply fungicide",
                "Avoid overwatering",
                "Use neem oil spray"
            ]
        }

    def apply_geo_filter(self, disease, region):
        possible = self.region_map.get(region, [])

        if disease not in possible:
            return f"{disease} (less common in your region)"
        return disease

    def get_treatment(self, disease):
        base = disease.split(" (")[0]
        return self.treatment_map.get(base, ["No data available"])