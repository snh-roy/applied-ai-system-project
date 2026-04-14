"""
Integration tests for RAG System
"""

import unittest
import sys
import os
import tempfile
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag.knowledge_base import MentalHealthKnowledgeBase, MentalHealthResource
from src.rag.retrieval import RAGSystem, SimpleRAGInterface


class TestRAGSystem(unittest.TestCase):
    """Test suite for RAG retrieval functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up RAG system once for all tests"""
        # Create temporary directory for ChromaDB
        cls.temp_dir = tempfile.mkdtemp()
        cls.rag_system = RAGSystem(persist_directory=cls.temp_dir)
        cls.simple_rag = SimpleRAGInterface(cls.rag_system)
        
    @classmethod
    def tearDownClass(cls):
        """Clean up temporary directory"""
        shutil.rmtree(cls.temp_dir)
        
    def test_knowledge_base_initialization(self):
        """Test that knowledge base loads resources correctly"""
        kb = self.rag_system.knowledge_base
        
        self.assertGreater(len(kb.resources), 0)
        
        # Check that resources have required fields
        for resource in kb.resources:
            self.assertIsNotNone(resource.id)
            self.assertIsNotNone(resource.title)
            self.assertIsNotNone(resource.content)
            self.assertIsNotNone(resource.category)
            self.assertIsInstance(resource.applicable_moods, list)
            self.assertIsInstance(resource.effectiveness_rating, float)
            
    def test_retrieval_by_mood(self):
        """Test retrieving resources by mood"""
        moods = ["anxious", "sad", "angry"]
        
        for mood in moods:
            resources = self.rag_system.retrieve_relevant_resources(
                query="I need help",
                mood=mood,
                n_results=3
            )
            
            # Should return some resources
            self.assertGreater(len(resources), 0)
            
            # Resources should be relevant to the mood
            for resource in resources:
                # Either mood is applicable or it's a general resource
                mood_relevant = (mood in resource.resource.applicable_moods or 
                               len(resource.resource.applicable_moods) > 3)
                self.assertTrue(mood_relevant)
                
    def test_retrieval_by_query(self):
        """Test semantic search retrieval"""
        queries = [
            ("breathing techniques for anxiety", "breathing"),
            ("how to stop worrying", "worry"),
            ("dealing with anger", "anger")
        ]
        
        for query, expected_keyword in queries:
            resources = self.rag_system.retrieve_relevant_resources(
                query=query,
                n_results=3
            )
            
            # Should return resources
            self.assertGreater(len(resources), 0)
            
            # At least one resource should contain the expected keyword
            found_keyword = False
            for resource in resources:
                if expected_keyword.lower() in resource.resource.content.lower():
                    found_keyword = True
                    break
            self.assertTrue(found_keyword, 
                          f"No resource found with keyword '{expected_keyword}' for query '{query}'")
            
    def test_retrieval_scoring(self):
        """Test that relevance scores are calculated correctly"""
        resources = self.rag_system.retrieve_relevant_resources(
            query="anxiety breathing exercises",
            mood="anxious",
            n_results=5
        )
        
        # Check scores are in descending order
        scores = [r.relevance_score for r in resources]
        self.assertEqual(scores, sorted(scores, reverse=True))
        
        # All scores should be positive
        for score in scores:
            self.assertGreater(score, 0)
            
    def test_contextual_response_generation(self):
        """Test response generation with context"""
        from src.core.mood_analyzer import EnhancedMoodAnalyzer
        
        analyzer = EnhancedMoodAnalyzer()
        mood_result = analyzer.analyze("I'm feeling very anxious")
        
        resources = self.rag_system.retrieve_relevant_resources(
            query="I'm feeling anxious",
            mood="anxious",
            n_results=3
        )
        
        response = self.rag_system.generate_contextual_response(
            query="I'm feeling anxious",
            mood_analysis=mood_result,
            retrieved_resources=resources
        )
        
        # Response should have required fields
        self.assertIn("response", response)
        self.assertIn("citations", response)
        self.assertIn("confidence", response)
        
        # Response should not be empty
        self.assertGreater(len(response["response"]), 0)
        
        # Should have citations
        self.assertGreater(len(response["citations"]), 0)
        
    def test_crisis_resources(self):
        """Test crisis resource retrieval"""
        crisis_info = self.rag_system.knowledge_base.get_crisis_resources()
        
        self.assertIn("hotlines", crisis_info)
        self.assertIn("immediate_steps", crisis_info)
        self.assertIn("safety_plan_template", crisis_info)
        
        # Check hotlines have required information
        for hotline in crisis_info["hotlines"]:
            self.assertIn("name", hotline)
            self.assertIn("number", hotline)
            self.assertIn("availability", hotline)
            
    def test_simple_interface(self):
        """Test simplified RAG interface"""
        response = self.simple_rag.get_support(
            user_input="I'm feeling overwhelmed and anxious",
            mood="anxious"
        )
        
        # Should return a string response
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        
        # Should mention recommended technique
        self.assertIn("recommend", response.lower())
        
    def test_empty_query_handling(self):
        """Test handling of empty queries"""
        resources = self.rag_system.retrieve_relevant_resources(
            query="",
            n_results=3
        )
        
        # Should still return some resources (based on mood or general)
        self.assertIsNotNone(resources)
        

class TestKnowledgeBase(unittest.TestCase):
    """Test knowledge base functionality"""
    
    def setUp(self):
        self.kb = MentalHealthKnowledgeBase()
        
    def test_resource_search(self):
        """Test searching resources by query"""
        results = self.kb.search_resources("breathing")
        
        self.assertGreater(len(results), 0)
        for resource in results:
            found = ("breathing" in resource.title.lower() or
                    "breathing" in resource.content.lower() or
                    "breathing" in [tag.lower() for tag in resource.tags])
            self.assertTrue(found)
            
    def test_coping_strategies(self):
        """Test retrieval of coping strategies"""
        moods = ["anxious", "sad", "angry", "stressed"]
        
        for mood in moods:
            strategies = self.kb.get_coping_strategies(mood)
            self.assertIsInstance(strategies, list)
            self.assertGreater(len(strategies), 0)
            
    def test_technique_info(self):
        """Test therapeutic technique information"""
        techniques = ["CBT", "DBT", "ACT"]
        
        for technique in techniques:
            info = self.kb.get_technique_info(technique)
            self.assertIsInstance(info, dict)
            self.assertIn("name", info)
            self.assertIn("techniques", info)
            self.assertIn("effective_for", info)
            
    def test_resource_effectiveness_ratings(self):
        """Test that all resources have valid effectiveness ratings"""
        for resource in self.kb.resources:
            self.assertGreaterEqual(resource.effectiveness_rating, 0.0)
            self.assertLessEqual(resource.effectiveness_rating, 1.0)
            

class TestRAGReliability(unittest.TestCase):
    """Test reliability and consistency of RAG system"""
    
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.rag_system = RAGSystem(persist_directory=cls.temp_dir)
        
    @classmethod  
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)
        
    def test_retrieval_consistency(self):
        """Test that same query returns consistent results"""
        query = "help with anxiety"
        mood = "anxious"
        
        results1 = self.rag_system.retrieve_relevant_resources(query, mood, n_results=3)
        results2 = self.rag_system.retrieve_relevant_resources(query, mood, n_results=3)
        
        # Should return same top resources
        ids1 = [r.resource.id for r in results1]
        ids2 = [r.resource.id for r in results2]
        
        self.assertEqual(ids1, ids2)
        
    def test_relevance_threshold(self):
        """Test that returned resources meet relevance threshold"""
        resources = self.rag_system.retrieve_relevant_resources(
            query="specific meditation technique for panic attacks",
            mood="anxious",
            n_results=5
        )
        
        for resource in resources:
            # All returned resources should have reasonable relevance
            self.assertGreater(resource.relevance_score, 0.1)
            

def run_tests():
    """Run all RAG tests and return summary"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestRAGSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeBase))
    suite.addTests(loader.loadTestsFromTestCase(TestRAGReliability))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return summary
    return {
        "total_tests": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "success_rate": (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    }


if __name__ == "__main__":
    summary = run_tests()
    print("\n" + "="*50)
    print("RAG SYSTEM TEST SUMMARY")
    print("="*50)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}") 
    print(f"Errors: {summary['errors']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print("="*50)