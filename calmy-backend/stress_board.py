from ai_model import predict_stress
from voice_analysis import predict_voice_stress
from temperature_analysis import predict_temp_stress

# Weights for each AI model
HRV_WEIGHT = 0.5
VOICE_WEIGHT = 0.3
TEMP_WEIGHT = 0.2

def calculate_stress_board (hrv_stress, voice_stress, temp_stress) -> float:
    """
    Calculate a final stress score based on weighted averages.
    Each model outputs a score between 0 and 1.
    """
    try:
        hrv_score = float(hrv_stress)  
        voice_score = float(voice_stress)  # Directly use passed voice_stress
        temp_score = float(temp_stress) 

        # Weighted stress score
        final_score = (
            (HRV_WEIGHT * hrv_score) +
            (VOICE_WEIGHT * voice_score) +
            (TEMP_WEIGHT * temp_score)
        )

        return round(final_score, 2) 
    
    except Exception as e:
        print(f"Error calculating stress score: {e}")
        return 0.0  # Return a default score in case of failure

