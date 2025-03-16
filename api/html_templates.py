import json


def generate_html_from_json(response: dict) -> str:
    """
    Generate HTML output based on the JSON response agent_type.
    
    Parameters:
    - response: JSON response from an agent
    
    Returns:
    - HTML string
    """
    agent_data = response.get("data")
    
    agent_type = agent_data.agent_type if agent_data else None

    print(f"Generating HTML for agent type: {agent_type}")
    
    if agent_type == "energy" or agent_type == "Energy Agent":
        country = agent_data.country if agent_data and agent_data.country else "Desconocido"
        data = agent_data.data if agent_data and agent_data.data else "No se encontraron datos."
        return f"""
            <div class="bg-green-100 p-6 rounded-lg shadow-lg border border-green-300">
                <h2 class="text-green-600 font-bold text-xl mb-2">Datos de Energía Renovable</h2>
                <p class="text-gray-700 mb-4">País: {country}</p>
                <pre class="bg-gray-100 p-4 rounded-lg text-sm font-mono">{data}</pre>
            </div>
            """
    
    elif agent_type == "Money Agent" or agent_type == "money":
        data = agent_data.data if agent_data and agent_data.data else "No se encontraron datos."
        return f"""
            <div class="bg-blue-100 p-6 rounded-lg shadow-lg border border-blue-300">
            <h2 class="text-blue-600 font-bold text-xl mb-2">Asesoramiento Financiero</h2>
            <p class="text-gray-700">{data}</p>
            </div>
            """
    
    elif agent_type == "Health Agent" or agent_type == "health":
        data = agent_data.data if agent_data and agent_data.data else "No se encontraron datos."
        return f"""
            <div class="bg-yellow-100 p-6 rounded-lg shadow-lg border border-yellow-300">
                <h2 class="text-yellow-600 font-bold text-xl mb-2">Datos de Salud</h2>
                <p class="text-gray-700 mb-2">Indicador: {data}</p> 
            </div>
            """
    
    elif agent_type == "Climate Agent" or agent_type == "climate":
        latitude = response.get("latitude", "Desconocido")
        longitude = response.get("longitude", "Desconocido")
        data = response.get("data", "No se encontraron datos.")
        if response.get("status") == "success":
            return f"""
            <div class="bg-teal-100 p-6 rounded-lg shadow-lg border border-teal-300">
                <h2 class="text-teal-600 font-bold text-xl mb-2">Datos Climáticos</h2>
                <p class="text-gray-700 mb-2">Latitud: {latitude}</p>
                <p class="text-gray-700 mb-4">Longitud: {longitude}</p>
                <pre class="bg-gray-100 p-4 rounded-lg text-sm font-mono">{data}</pre>
            </div>
            """
        else:
            message = response.get("message", "Error desconocido.")
            return f"""
            <div class="bg-red-100 p-6 rounded-lg shadow-lg border border-red-300">
                <h2 class="text-red-600 font-bold text-xl mb-2">Error en Clima</h2>
                <p class="text-gray-700">{message}</p>
            </div>
            """
    
    elif agent_type == "Final Output Agent" or agent_type == "final":
        problems = response.get("problems", [])
        recommendations = response.get("recommendations", [])
        user_data = response.get("user_data", {})
        
        user_info = f"""
        <div class="bg-gray-100 p-6 rounded-lg shadow-lg border border-gray-300 mb-6">
            <h2 class="text-gray-600 font-bold text-xl mb-2">Información del Usuario</h2>
            <pre class="bg-white p-4 rounded-lg text-sm font-mono">{json.dumps(user_data, indent=2, ensure_ascii=False)}</pre>
        </div>
        """ if user_data else ""
        
        problems_html = "".join(
            f'<li class="mb-2 p-2 bg-red-100 rounded-lg shadow-sm border border-red-200">{problem}</li>' for problem in problems
        ) if problems else "<li>No se identificaron problemas.</li>"
        
        recommendations_html = "".join(
            f'<li class="mb-2 p-2 bg-green-100 rounded-lg shadow-sm border border-green-200">{rec}</li>' for rec in recommendations
        ) if recommendations else "<li>No hay recomendaciones disponibles.</li>"
        
        return f"""
        <div class="bg-white p-8 rounded-lg shadow-xl border border-gray-200">
            <h1 class="text-2xl font-bold text-blue-600 mb-6">Resumen Final</h1>
            {user_info}
            <div class="mb-6">
                <h2 class="text-xl font-bold text-red-600 mb-2">Problemas Identificados</h2>
                <ul class="list-disc pl-6">{problems_html}</ul>
            </div>
            <div>
                <h2 class="text-xl font-bold text-green-600 mb-2">Recomendaciones</h2>
                <ul class="list-disc pl-6">{recommendations_html}</ul>
            </div>
        </div>
        """
    
    elif agent_type == "Main Agent" or agent_type == "main":
        data = agent_data.data if agent_data and agent_data.data else "No se encontraron datos."
        return f"""
            <div class="bg-blue-100 p-6 rounded-lg shadow-lg border border-blue-300">
                <h2 class="text-blue-600 font-bold text-xl mb-2">Respuesta del Agente Principal</h2>
                <p class="text-gray-700">{data}</p>
            </div>
            """
    
    elif agent_type == "Government Agent" or agent_type == "government":
        country = agent_data.country if agent_data and agent_data.country else "Desconocido"
        city = agent_data.city if agent_data and agent_data.city else "Desconocido"
        data = agent_data.data if agent_data and agent_data.data else "No se encontraron datos."
        return f"""
            <div class="bg-purple-100 p-6 rounded-lg shadow-lg border border-purple-300">
                <h2 class="text-purple-600 font-bold text-xl mb-2">Información Gubernamental</h2>
                <p class="text-gray-700 mb-2">País: {country}</p>
                <p class="text-gray-700 mb-4">Ciudad: {city}</p>
                <pre class="bg-gray-100 p-4 rounded-lg text-sm font-mono">{data}</pre>
            </div>
            """
    
    elif agent_type == "Emigration Agent" or agent_type == "emigration":
        data = agent_data.data if agent_data and agent_data.data else "No se encontraron datos."
        return f"""
            <div class="bg-orange-100 p-6 rounded-lg shadow-lg border border-orange-300">
                <h2 class="text-orange-600 font-bold text-xl mb-2">Asistencia de Emigración</h2>
                <p class="text-gray-700">{data}</p>
            </div>
            """
    
    else:
        return f"""
        <div class="bg-gray-100 p-6 rounded-lg shadow-lg border border-gray-300">
            <h2 class="text-gray-600 font-bold text-xl mb-2">Respuesta Desconocida</h2>
            <p class="text-gray-700">No se pudo determinar el tipo de respuesta.</p>
        </div>
        """
