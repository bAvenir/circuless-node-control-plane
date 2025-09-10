# DCAT SCHEMA for Node descriptions

node = {
  "@context": [
    "https://www.w3.org/ns/dcat#",
    "https://w3id.org/dc/terms/",
    {
      "dcat": "https://www.w3.org/ns/dcat#",
      "dcterms": "https://purl.org/dc/terms/",
      "ids": "https://w3id.org/idsa/core/",
      "eu": "https://data.europa.eu/eli/ontology#"
    }
  ],
  "@id": "https://example.com/dataconnector/connector-1234",
  "@type": "dcat:DataService",
  "dcterms:title": "Sample EU Data Space Connector",
  "dcterms:description": "A data connector service to enable secure and controlled data sharing in the EU Data Space.",
  "dcat:landingPage": "https://example.com/dataconnector/docs",
  "dcat:servesDataset": {
    "@id": "https://example.com/dataset/sample-dataset",
    "@type": "dcat:Dataset",
    "dcterms:title": "Sample Dataset",
    "dcterms:description": "A sample dataset available via the data connector.",
    "dcat:distribution": {
      "@type": "dcat:Distribution",
      "dcat:accessURL": "https://example.com/dataset/sample-dataset/data",
      "dcat:mediaType": "application/json",
      "dcterms:license": "https://data.europa.eu/eli/cc/by/4.0/"
    }
  },
  "ids:resourceEndpoint": {
    "@type": "ids:Resource",
    "ids:accessURL": "https://example.com/dataconnector/api",
    "ids:accessUrl": "https://example.com/dataconnector/api"
  },
  "ids:securityProfile": "https://w3id.org/idsa/code#BaseSecurityProfile",
  "eu:compliance": "https://data.europa.eu/eli/regulation/2018/1725/oj",
  "dcat:contactPoint": {
    "@type": "vcard:Email",
    "vcard:value": "mailto:contact@example.com"
  }
}
