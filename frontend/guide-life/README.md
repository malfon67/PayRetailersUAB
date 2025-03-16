# Guide Life Frontend

This is the front-end application for the Guide Life project, built using **React** and styled with **Tailwind CSS**. The application provides an interactive user interface for features like chat, audio recording, and data visualization.

## Features

- **Chat Interface**: A conversational interface with AI responses.
- **Audio Recorder**: Record and upload audio for processing.
- **Dynamic Summaries**: Display positive and negative points based on AI analysis.
- **Responsive Design**: Styled with Tailwind CSS for a modern and responsive UI.

## Project Structure

- **`src`**: Contains the main React components and pages.
  - **`pagines`**: Includes key pages like `chat.tsx`, `audioRecorder.tsx`, and `summary.tsx`.
  - **`components`**: Reusable components like `userInput_API` and `userAudio_API`.
  - **`App.tsx`**: Main entry point for the application.
- **`public`**: Static assets and configuration files.
  - **`lib`**: Includes JSON data files like `countriesWithCities.json` and utility scripts like `fetching.js`.
  - **`tailwind.css`**: Tailwind CSS configuration for styling.
- **`tailwind.config.js`**: Tailwind CSS configuration file.
- **`postcss.config.js`**: PostCSS configuration for processing CSS.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd guide-life
   ```

2. **Install Dependencies**:
   Ensure you have Node.js installed, then run:
   ```bash
   npm install
   ```

3. **Run the Development Server**:
   Start the application locally:
   ```bash
   npm start
   ```

4. **Build for Production**:
   Create a production-ready build:
   ```bash
   npm run build
   ```

## Key Dependencies

- **React**: For building the user interface.
- **Tailwind CSS**: For styling.
- **React Router**: For navigation between pages.
- **TypeScript**: For type safety and better development experience.

## Scripts

- `npm start`: Runs the app in development mode.
- `npm run build`: Builds the app for production.
- `npm test`: Runs the test suite.

## Notes

- The `countriesWithCities.json` file contains geographical data used in the application.
- The `fetching.js` script demonstrates how to fetch and process data from external APIs.

## Contributing

Feel free to fork the repository and submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.

