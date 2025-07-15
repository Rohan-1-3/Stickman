from slider import LabeledSlider

sliders = [
    LabeledSlider("Head Size", 50, 50, 200, 20, 100, 50),
    LabeledSlider("Eye Size", 50, 100, 200, 1, 20, 6),
    LabeledSlider("Nose Size", 50, 150, 200, 2, 20, 8),
    LabeledSlider("Mouth Size", 50, 200, 200, 5, 40, 20),
    LabeledSlider("Arm Length", 50, 250, 200, 20, 150, 80),
    LabeledSlider("Arm Thickness", 50, 300, 200, 1, 10, 6),
    LabeledSlider("Torso Length", 50, 350, 200, 30, 150, 100),
    LabeledSlider("Leg Length", 50, 400, 200, 30, 150, 100),
]

def get_stickman_config_from_sliders():
    return {
        "head_size": sliders[0].value,
        "eye_size": sliders[1].value,
        "nose_size": sliders[2].value,
        "mouth_size": sliders[3].value,
        "arm_length": sliders[4].value,
        "arm_thickness": sliders[5].value,
        "torso_length": sliders[6].value,
        "leg_length": sliders[7].value,
        "hair_color": (100, 0, 100),
        "skin_color": (255, 224, 189)
    }
