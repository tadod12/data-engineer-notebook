# Chapter 11 Code Note
## Testing your code
### Syntax
1. unittest
    ```
   import unittest
   from name_function import get_formatted_name  # test function get_formatted_name()
   
   class NamesTestCase(unittest.TestCase):
    
      def test_first_last_name(self):
         formatted_name = get_formatted_name('janis', 'joplin')
         self.assertEqual(formatted_name, 'Janis Joplin')
   
      def test_first_last_middle_name(self):
         formatted_name = get_formatted_name('wolfgang', 'mozart', 'amadeus')
         self.assertEqual(formatted_name, 'Wolfgang Amadeus Mozart')
   
   if __name__ = '__main__':  # only run if this file is the main program (run directly)
      unittest.main()  # run all def starting with 'test_' in the name
   ```
   
2. The setUp() method
   ```
   import unittest
   from survey import AnonymousSurvey
   
   class TestAnonymousSurvey(unittest.TestCase):
      def setUp(self):
         question = 'What language did you first learn to speak? '
         self.my_survey = AnonymousSurvey(question)
         self.responses = ['English', 'Spanish', 'Mandarin']
   
      def test_store_single_response(self):
         self.my_survey.store_response(self.responses[0])
         self.assertIn(self.responses[0], self.my_survey.responses)
   
      def test_store_three_responses(self):
         for response in self.responses:
            self.my_survey.store_response(response)
         for response in self.responses:
            self.assertIn(response, self.my_survey.responses)
   
   if __name__ == '__main__':
      unittest.main()
   ```
   > Python runs the `setUp()` method before running each method starting with 'test_'

