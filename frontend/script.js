const API_URL = "http://127.0.0.1:8000";

const generateBtn = document.getElementById('generate-btn');
const topicInput = document.getElementById('topic-input');
const loadingIndicator = document.getElementById('loading-indicator');
const loadingText = document.getElementById('loading-text');
const researchersSection = document.getElementById('researchers-section');
const researchersGrid = document.getElementById('researchers-grid');
const resultsSection = document.getElementById('results-section');
const reportContent = document.getElementById('report-content');
const conversationContent = document.getElementById('conversation-content');

let currentTopic = "";

// 1. Generate Researchers
generateBtn.addEventListener('click', async () => {
    currentTopic = topicInput.value.trim();
    if (!currentTopic) return alert("Please enter a topic!");

    // UI Updates
    researchersSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    loadingIndicator.classList.remove('hidden');
    loadingText.innerText = "Assembling your researchers...";

    try {
        const response = await fetch(`${API_URL}/create_researchers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: currentTopic, max_researchers: 3 })
        });
        
        const data = await response.json();
        renderResearchers(data.researchers);
        
    } catch (error) {
        alert("Error connecting to backend! Is your FastAPI server running?");
        console.error(error);
    } finally {
        loadingIndicator.classList.add('hidden');
    }
});

// 2. Display the Researchers
function renderResearchers(researchers) {
    researchersGrid.innerHTML = ""; // Clear old data
    
    researchers.forEach(researcher => {
        const card = document.createElement('div');
        card.className = 'researcher-card';
        card.innerHTML = `
            <h3>${researcher.name}</h3>
            <div class="role">${researcher.role}</div>
            <p><strong>Interests:</strong> ${researcher.research_interests}</p>
            <p><strong>CV:</strong> ${researcher.CV}</p>
        `;
        
        // When clicked, start the research!
        card.addEventListener('click', () => runResearch(researcher));
        researchersGrid.appendChild(card);
    });

    researchersSection.classList.remove('hidden');
}

// 3. Run the LangGraph QA Loop
async function runResearch(researcher) {
    researchersSection.classList.add('hidden');
    loadingIndicator.classList.remove('hidden');
    loadingText.innerText = `${researcher.name} is researching and writing the report. This may take a minute...`;

    try {
        const response = await fetch(`${API_URL}/run_research`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: currentTopic, researcher: researcher })
        });
        
        const data = await response.json();
        
        // Parse Markdown to HTML for the report
        reportContent.innerHTML = marked.parse(data.report);
        
        // Format the conversation
        conversationContent.innerHTML = data.conversation.map(msg => 
            `<p><strong>${msg.includes('question:') ? 'Researcher' : 'Expert'}:</strong> ${msg.replace('question:', '').replace('answer:', '')}</p>`
        ).join('<hr>');

        resultsSection.classList.remove('hidden');
        
    } catch (error) {
        alert("Error during research process!");
        console.error(error);
    } finally {
        loadingIndicator.classList.add('hidden');
    }
}

// Tab Switching Logic
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active-content'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(`${tabName}-content`).classList.add('active-content');
    event.target.classList.add('active');
}