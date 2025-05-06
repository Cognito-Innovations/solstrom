const API_URL = process.env.REACT_APP_API_URL;

export const sendMessage = async (message: string) => {
  try {
    const response = await fetch(`${API_URL}/agent/conversation`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    return data.conversation.response;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};