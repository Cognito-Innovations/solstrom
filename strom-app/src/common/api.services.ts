const API_URL = process.env.REACT_APP_API_URL;

export const sendMessage = async (message: string, user?: any) => {
  try {
    const body: any = { message };
    if (user) body.user = user;
    const response = await fetch(`${API_URL}/agent/conversation`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error sending message:", error);
    throw error;
  }
};

export const loginWithGoogle = async (token: string) => {
  try {
    const response = await fetch(`${API_URL}/agent/auth/google`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Google login failed");
    }
    
    const data = await response.json();
    return data;

  } catch (error) {
    console.error("Error during Google login:", error);
    throw error;
  }
};

export const handlePayment = async (userId: string) => {
  const response = await fetch(`${API_URL}/agent/user/pay`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId })
  });

  if (!response.ok) {
    throw new Error("Payment failed");
  }

  return await response.json();
};
