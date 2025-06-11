const API_URL = 'http://localhost:8000/api/ask'; // Update with your backend URL

export const sendQuestion = async (question) => {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });
        const data = await response.json();
        return data.answer; // Adjust based on your backend response structure
    } catch (error) {
        console.error("Error sending question:", error);
        return "Sorry, there was an error.";
    }
};
