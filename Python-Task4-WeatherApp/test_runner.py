"""
Automated Unit Test Suite for Basic Weather App
Tests temperature unit conversion, input validation, and weather service geocoding.
"""

import unittest
import weather_service

class TestWeatherApp(unittest.TestCase):

    # 1. Temperature Conversion Tests
    def test_celsius_to_fahrenheit(self):
        self.assertEqual(weather_service.celsius_to_fahrenheit(0), 32.0)
        self.assertEqual(weather_service.celsius_to_fahrenheit(100), 212.0)
        self.assertEqual(weather_service.celsius_to_fahrenheit(20), 68.0)

    def test_fahrenheit_to_celsius(self):
        self.assertEqual(weather_service.fahrenheit_to_celsius(32), 0.0)
        self.assertEqual(weather_service.fahrenheit_to_celsius(212), 100.0)
        self.assertEqual(weather_service.fahrenheit_to_celsius(68), 20.0)

    # 2. Input Validation Tests
    def test_empty_query_validation(self):
        success, result = weather_service.get_weather("")
        self.assertFalse(success)
        self.assertIn("valid city name", result)

        success2, result2 = weather_service.get_weather("   ")
        self.assertFalse(success2)
        self.assertIn("valid city name", result2)

    # 3. WMO Weather Code Mapping Test
    def test_wmo_code_mapping(self):
        cond, icon = weather_service.WMO_CODE_MAP(0)
        self.assertEqual(cond, "Clear Sky")
        self.assertEqual(icon, "☀️")

        cond2, icon2 = weather_service.WMO_CODE_MAP(95)
        self.assertEqual(cond2, "Thunderstorm")
        self.assertEqual(icon2, "⛈️")

    # 4. Weather Search & Fallback Test
    def test_weather_search_known_city(self):
        success, data = weather_service.get_weather("London")
        self.assertTrue(success, f"Search failed with error: {data}")
        self.assertIn("city", data)
        self.assertEqual(data["city"], "London")
        self.assertIn("temp_c", data)
        self.assertIn("temp_f", data)
        self.assertIn("humidity", data)
        self.assertIn("hourly", data)
        self.assertIn("daily", data)
        self.assertTrue(len(data["hourly"]) > 0)
        self.assertTrue(len(data["daily"]) > 0)

if __name__ == "__main__":
    unittest.main()
