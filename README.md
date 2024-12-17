![IMG_7760](https://github.com/user-attachments/assets/86ebfee5-16e9-483c-970a-82c8e0775c4b)

>Mirach (Star), photographed by me in 2022 using Slooh and SloohManager

# SloohManager

A scheduling manager, mission log, and telescope dashboard integrated with the [Slooh](https://www.slooh.com/) platform, seamlessly synchronized with your Notion workspaces.

## Overview

This project aims to automate the process of fetching mission schedules and telescope availability from the Slooh platform using Selenium for web scraping, and seamlessly synchronize the data with the user's Notion databases.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Dependencies](#dependencies)
- [Contributing](#contributing)

## Features

### Telescope Availability

- **Telescope Status**: The project actively monitors and fetches the live status of telescopes available on the Slooh platform, providing real-time updates on telescope availability and operational status.

![image](https://github.com/maxk7/SloohManager/assets/43018603/171c8930-bba6-4eb3-89e3-a6fc8af8afa8)

### Mission Management

- **Basic Missions**: The project fetches basic missions from the Slooh platform, capturing details such as the mission target, scheduled time, associated telescope, and status message (if available).
  
- **Advanced Missions**: In addition to basic missions, the project also retrieves advanced missions, providing insights into more complex or specialized missions.
  
- **Recent Missions**: The project fetches recently completed or ongoing missions from the Slooh platform, allowing users to monitor the latest activities and statuses.

#### Upcoming missions view
![image](https://github.com/maxk7/SloohManager/assets/43018603/d3007106-2619-4298-83cc-6c28aec11899)

#### Previous missions view
![image](https://github.com/maxk7/SloohManager/assets/43018603/d652229a-ba1e-4631-b08f-15e874e6a3de)

#### View the status of an individual mission
![image](https://github.com/maxk7/SloohManager/assets/43018603/2bdaab2a-ba97-46b5-bb8b-7ba000f39587)

### Selenium Integration

- **Automated Web Scraping**: The project utilizes Selenium for automated web scraping, enabling seamless interaction with the Slooh platform to fetch mission schedules and telescope availability details.

### Dynamic Data Formatting

- **Mission Formatting**: The project dynamically formats mission schedules, categorizing missions into basic and advanced categories, and presenting them in a structured manner for easy viewing and analysis.

- **Telescope Availability Mapping**: The project maps telescope availability details, presenting the data in an organized format that allows users to quickly assess the status of different telescopes.

### Integration with Notion Databases

- **Seamless Data Synchronization**: The project seamlessly integrates with the user's Notion databases, allowing for the automatic synchronization of mission schedules and details. This integration ensures that mission data remains consistent and up-to-date across both platforms.

- **Customizable Data Mapping**: The integration with Notion databases offers flexible data mapping capabilities, allowing users to customize how mission and telescope availability data is structured and organized within their Notion workspace.

- **Automated Data Updates**: The project supports automated data updates, periodically fetching new mission schedules and telescope availability details and updating the corresponding Notion databases.

- **Enhanced Collaboration and Accessibility**: By integrating with Notion databases, the project promotes enhanced collaboration by providing a centralized platform where team members can access and collaborate on mission and telescope data.

## Dependencies

- Python
- Selenium
- ChromeDriver (based on operating system)
- YAML

## Contributing
Feel free to fork the repository and submit pull requests with your enhancements or bug fixes.
