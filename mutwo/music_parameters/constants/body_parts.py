__all__ = ("ANATOMY",)

ANATOMY = r"""
- id_list:
    - Left
    - Right
  name: side
  item_list:
    - id_list:
        - Arm
      name: limb
      item_list:
        - id_list:
            - Hand
          name: appendage
          item_list:
              - id_list:
                    - Finger
                    - Stick
                name: digit
                item_list:
                    - One
                    - Two
                    - Three
                    - Four
                    - Five
"""
"""Default anatomy for `mutwo.music_parameters.constants.BODY`."""
