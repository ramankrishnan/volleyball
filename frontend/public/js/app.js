// API Base URL
const API_BASE = '/api';

// === Utility Functions ===
function showMessage(containerId, message, type) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="message ${type}">${message}</div>`;
        setTimeout(() => {
            container.innerHTML = '';
        }, 5000);
    }
}

async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    if (data) {
        options.body = JSON.stringify(data);
    }
    const response = await fetch(`${API_BASE}${endpoint}`, options);
    return response.json();
}

// === Team Functions ===
async function loadTeams() {
    try {
        const teams = await apiCall('/teams');
        return teams;
    } catch (error) {
        console.error('Error loading teams:', error);
        return [];
    }
}

async function displayTeams() {
    const container = document.getElementById('teams-table-body');
    if (!container) return;
    
    container.innerHTML = '<tr><td colspan="7" class="loading">Loading teams</td></tr>';
    
    try {
        const teams = await loadTeams();
        
        if (teams.length === 0) {
            container.innerHTML = '<tr><td colspan="7" style="text-align:center;color:#aaa;padding:30px;">No teams registered yet</td></tr>';
            return;
        }
        
        container.innerHTML = teams.map(team => `
            <tr>
                <td>${team.id}</td>
                <td><strong>${team.team_name}</strong></td>
                <td>${team.captain_name}</td>
                <td>${team.email}</td>
                <td>${team.phone}</td>
                <td>${team.players_count}</td>
                <td>
                    <button class="btn btn-danger btn-small" onclick="deleteTeam(${team.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        container.innerHTML = '<tr><td colspan="7" style="text-align:center;color:#e74c3c;">Error loading teams</td></tr>';
    }
}

async function registerTeam(event) {
    event.preventDefault();
    
    const data = {
        team_name: document.getElementById('team_name').value,
        captain_name: document.getElementById('captain_name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        players_count: parseInt(document.getElementById('players_count').value),
    };
    
    try {
        const result = await apiCall('/teams', 'POST', data);
        if (result.id) {
            showMessage('form-message', '🎉 Team registered successfully!', 'success');
            document.getElementById('register-form').reset();
        } else {
            showMessage('form-message', result.error || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage('form-message', 'Error registering team. Please try again.', 'error');
    }
}

async function deleteTeam(teamId) {
    if (!confirm('Are you sure you want to delete this team?')) return;
    
    try {
        await apiCall(`/teams/${teamId}`, 'DELETE');
        displayTeams();
    } catch (error) {
        alert('Error deleting team');
    }
}

// === Match Functions ===
async function displayMatches() {
    const container = document.getElementById('matches-container');
    if (!container) return;
    
    container.innerHTML = '<div class="loading">Loading matches</div>';
    
    try {
        const matches = await apiCall('/matches');
        
        if (matches.length === 0) {
            container.innerHTML = '<div style="text-align:center;color:#aaa;padding:40px;">No matches scheduled yet</div>';
            return;
        }
        
        container.innerHTML = '<div class="matches-grid">' + matches.map(match => `
            <div class="match-card">
                <div class="match-header">
                    <span>Match #${match.id}</span>
                    <span class="status ${match.status}">${match.status}</span>
                </div>
                <div class="teams">
                    <div class="team">
                        <h3>${match.team1_name}</h3>
                        <div class="score">${match.score_team1}</div>
                    </div>
                    <div class="vs">VS</div>
                    <div class="team">
                        <h3>${match.team2_name}</h3>
                        <div class="score">${match.score_team2}</div>
                    </div>
                </div>
                <div class="match-info">
                    <span>📅 ${match.match_date}</span>
                    <span>⏰ ${match.match_time}</span>
                    <span>📍 ${match.location}</span>
                </div>
                <div class="match-actions">
                    <button class="btn btn-success btn-small" onclick="updateScore(${match.id})">Update Score</button>
                    <button class="btn btn-danger btn-small" onclick="deleteMatch(${match.id})">Delete</button>
                </div>
            </div>
        `).join('') + '</div>';
    } catch (error) {
        container.innerHTML = '<div style="text-align:center;color:#e74c3c;">Error loading matches</div>';
    }
}

async function loadTeamOptions() {
    const select1 = document.getElementById('team1_id');
    const select2 = document.getElementById('team2_id');
    if (!select1 || !select2) return;
    
    try {
        const teams = await loadTeams();
        const options = teams.map(t => `<option value="${t.id}">${t.team_name}</option>`).join('');
        select1.innerHTML = '<option value="">Select Team 1</option>' + options;
        select2.innerHTML = '<option value="">Select Team 2</option>' + options;
    } catch (error) {
        console.error('Error loading team options:', error);
    }
}

async function scheduleMatch(event) {
    event.preventDefault();
    
    const data = {
        team1_id: parseInt(document.getElementById('team1_id').value),
        team2_id: parseInt(document.getElementById('team2_id').value),
        match_date: document.getElementById('match_date').value,
        match_time: document.getElementById('match_time').value,
        location: document.getElementById('location').value,
    };
    
    try {
        const result = await apiCall('/matches', 'POST', data);
        if (result.id) {
            showMessage('match-message', '🏐 Match scheduled successfully!', 'success');
            document.getElementById('match-form').reset();
            displayMatches();
        } else {
            showMessage('match-message', result.error || 'Failed to schedule match', 'error');
        }
    } catch (error) {
        showMessage('match-message', 'Error scheduling match. Please try again.', 'error');
    }
}

async function updateScore(matchId) {
    const score1 = prompt('Enter score for Team 1:');
    if (score1 === null) return;
    const score2 = prompt('Enter score for Team 2:');
    if (score2 === null) return;
    const status = prompt('Enter status (scheduled/live/completed):', 'completed');
    if (status === null) return;
    
    try {
        await apiCall(`/matches/${matchId}/score`, 'PUT', {
            score_team1: parseInt(score1),
            score_team2: parseInt(score2),
            status: status
        });
        displayMatches();
    } catch (error) {
        alert('Error updating score');
    }
}

async function deleteMatch(matchId) {
    if (!confirm('Are you sure you want to delete this match?')) return;
    
    try {
        await apiCall(`/matches/${matchId}`, 'DELETE');
        displayMatches();
    } catch (error) {
        alert('Error deleting match');
    }
}

// === Dashboard Stats ===
async function loadDashboardStats() {
    const teamsCount = document.getElementById('teams-count');
    const matchesCount = document.getElementById('matches-count');
    
    try {
        const teams = await loadTeams();
        const matches = await apiCall('/matches');
        
        if (teamsCount) teamsCount.textContent = teams.length;
        if (matchesCount) matchesCount.textContent = matches.length;
        
        const completedCount = document.getElementById('completed-count');
        if (completedCount) {
            completedCount.textContent = matches.filter(m => m.status === 'completed').length;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}