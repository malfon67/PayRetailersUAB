def generate_html_from_json(response: dict) -> str:
    """
    Generate HTML output based on the JSON response agent_type.
    
    Parameters:
    - response: JSON response from an agent
    
    Returns:
    - HTML string
    """
    agent_type = response.get("agent_type", "unknown")
    
    if agent_type == "energy":
        if response["status"] == "success":
            return f"""
            <div class="bg-green-100 p-4 rounded-lg">
                <h2 class="text-green-600 font-bold">Datos de Energía Renovable</h2>
                <p>País: {response.get('country')}</p>
                <pre class="bg-gray-100 p-2 rounded">{response.get('data')}</pre>
            </div>
            """
        else:
            return f"""
            <div class="bg-red-100 p-4 rounded-lg">
                <h2 class="text-red-600 font-bold">Error en Energía</h2>
                <p>{response.get('message')}</p>
            </div>
            """
    
    elif agent_type == "money":
        if response["status"] == "success":
            return f"""
            <div class="bg-blue-100 p-4 rounded-lg">
                <h2 class="text-blue-600 font-bold">Asesoramiento Financiero</h2>
                <p>{response.get('advice')}</p>
            </div>
            """
        else:
            return f"""
            <div class="bg-red-100 p-4 rounded-lg">
                <h2 class="text-red-600 font-bold">Error en Finanzas</h2>
                <p>{response.get('message')}</p>
            </div>
            """
    
    elif agent_type == "health":
        if response["status"] == "success":
            return f"""
            <div class="bg-yellow-100 p-4 rounded-lg">
                <h2 class="text-yellow-600 font-bold">Datos de Salud</h2>
                <p>Indicador: {response.get('indicator')}</p>
                <p>Valor: {response.get('value')}</p>
            </div>
            """
        else:
            return f"""
            <div class="bg-red-100 p-4 rounded-lg">
                <h2 class="text-red-600 font-bold">Error en Salud</h2>
                <p>{response.get('message')}</p>
            </div>
            """
    
    elif agent_type == "climate":
        if response["status"] == "success":
            return f"""
            <div class="bg-teal-100 p-4 rounded-lg">
                <h2 class="text-teal-600 font-bold">Datos Climáticos</h2>
                <p>Latitud: {response.get('latitude')}</p>
                <p>Longitud: {response.get('longitude')}</p>
                <pre class="bg-gray-100 p-2 rounded">{response.get('data')}</pre>
            </div>
            """
        else:
            return f"""
            <div class="bg-red-100 p-4 rounded-lg">
                <h2 class="text-red-600 font-bold">Error en Clima</h2>
                <p>{response.get('message')}</p>
            </div>
            """
    
    elif agent_type == "final_summary":
        problems = response.get("problems", [])
        recommendations = response.get("recommendations", [])
        user_data = response.get("user_data", {})
        
        user_info = ""
        if user_data:
            user_info = f"""
            <div class="bg-gray-100 p-4 rounded-lg mb-4">
                <h2 class="text-gray-600 font-bold">Información del Usuario</h2>
                <pre class="bg-white p-2 rounded">{json.dumps(user_data, indent=2, ensure_ascii=False)}</pre>
            </div>
            """
        
        problems_html = "".join(
            f'<li class="mb-2 p-2 bg-red-100 rounded">{problem}</li>' for problem in problems
        )
        recommendations_html = "".join(
            f'<li class="mb-2 p-2 bg-green-100 rounded">{rec}</li>' for rec in recommendations
        )
        
        return f"""
        <div class="bg-white p-6 rounded-lg shadow-md">
            <h1 class="text-2xl font-bold text-blue-600 mb-4">Resumen Final</h1>
            {user_info}
            <div class="mb-4">
                <h2 class="text-xl font-bold text-red-600">Problemas Identificados</h2>
                <ul class="list-disc pl-5">{problems_html}</ul>
            </div>
            <div>
                <h2 class="text-xl font-bold text-green-600">Recomendaciones</h2>
                <ul class="list-disc pl-5">{recommendations_html}</ul>
            </div>
        </div>
        """
    
    elif agent_type == "main":
        return f"""
            <div class="bg-blue-100 p-4 rounded-lg">
                <h2 class="text-blue-600 font-bold">Respuesta del Agente Principal</h2>
                <p>{response.get('data')}</p>
            </div>
            """
    
    else:
        return f"""
        <div class="bg-gray-100 p-4 rounded-lg">
            <h2 class="text-gray-600 font-bold">Respuesta Desconocida</h2>
            <p>No se pudo determinar el tipo de respuesta.</p>
        </div>
        """
