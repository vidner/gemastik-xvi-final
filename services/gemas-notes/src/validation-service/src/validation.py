validation_schema = {
    "/api/register": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "minLength": 5,
                "maxLength": 10,
                "format": "security-validation"
            },
            "email": {
                "type": "string",
                "format": "email"
            },
            "password": {
                "type": "string",
                "minLength": 10,
                "format": "security-validation"
            }
        }
    },
    "/api/login": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "format": "email"
            },
            "password": {
                "type": "string",
                "minLength": 10,
                "format": "security-validation"
            }
        }
    },
    "/api/notes": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "maxLength": 100,
                "format": "security-validation"
            },
            "content": {
                "type": "string",
                "minLength": 10,
                "format": "security-validation"
            },
            "tags": {
                "type": "string",
                "maxLength": 100,
                "format": "security-validation"
            }
        }
    },
    "/api/notes/count": {
        "type": "object",
        "properties": {
            "count_by": {
                "type": "string",
                "enum": ["title", "tags"]
            },
            "keyword": {
                "type": "string",
                "maxLength": 10,
                "format": "security-validation"
            }
        }
    }
}
