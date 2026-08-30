import os
from neo4j import GraphDatabase
from engines.graph.schemas import CompanyNodeCreate, RelationshipCreate

# Default local Neo4j connection parameters (can be overridden via environment variables)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class KnowledgeGraphService:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def create_company(self, data: CompanyNodeCreate):
        query = """
        MERGE (c:Company {name: $name})
        SET c.industry = $industry, c.jurisdiction = $jurisdiction
        RETURN c.name AS name
        """
        with self.driver.session() as session:
            result = session.run(query, name=data.name, industry=data.industry, jurisdiction=data.jurisdiction)
            return result.single()

    def create_relationship(self, data: RelationshipCreate):
        # Validate allowed relationship types for compliance
        allowed_types = {"OWNS", "BUYS_FROM", "SEALS_TO", "HAS_LOAN", "HAS_DIRECTOR"}
        if data.rel_type not in allowed_types and data.rel_type != "SELLS_TO":
            raise ValueError(f"Invalid relationship type: {data.rel_type}")

        query = f"""
        MATCH (a:Company {{name: $source}})
        MATCH (b:Company {{name: $target}})
        MERGE (a)-[r:{data.rel_type}]->(b)
        SET r.value = $value
        RETURN type(r) AS rel_type
        """
        with self.driver.session() as session:
            result = session.run(query, source=data.source_company, target=data.target_company, value=data.value)
            record = result.single()
            if not record:
                raise ValueError("Source or target company node not found in the graph.")
            return record

kg_service = KnowledgeGraphService()