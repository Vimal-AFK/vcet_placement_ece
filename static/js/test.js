function start() {
    document.getElementById('notice').style.display = 'none'; 
    document.getElementById('test').style.display = 'flex'; 

    const timerElement = document.getElementById('timer');
    let totalTime = 300;

    function updateTimer() {
        const minutes = Math.floor(totalTime / 60);
        const seconds = totalTime % 60;
        timerElement.textContent = `Time Remaining: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        if (totalTime > 0) {
            totalTime--;
            setTimeout(updateTimer, 1000);
        } else {
            alert('Time is up!');
        }
    }

    updateTimer();

    // Generate question boxes dynamically
    const questionBoxesContainer = document.getElementById('question-boxes');
    const numberOfQuestions = 10; // Example: 10 questions

    for (let i = 1; i <= numberOfQuestions; i++) {
        const box = document.createElement('div');
        box.className = 'box';
        box.textContent = i;
        questionBoxesContainer.appendChild(box);
    }

    // Submit button functionality
    document.getElementById('submit-btn').addEventListener('click', () => {
        alert('Test submitted successfully!');
    });
}

// Ensure the start function is called when the "Start Test" button is clicked
document.getElementById('start-btn').addEventListener('click', start);

// Ensure the notice div is visible initially
document.getElementById('notice').style.display = 'block';