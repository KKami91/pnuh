///import stress240401 from "./stress_score_2024-04-01.png";

const TestPage = () => {
    return (
      <div className="p-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to Stress Page</h1>
        <p className="text-lg mb-8">This is a sample page created using Next.js, TypeScript, and Tailwind CSS.</p>
        <button className="bg-blue-400 hover:bg-blue-700 text-red-500 font-bold py-2 px-5 rounded">
          Click me
        </button>
        <img src={"./stress_score/stress_score_2024-04-01.png"} alt="----"/>
        <img src={"./stress_score/stress_score_2024-04-02.png"} alt="stress_"/>
        <img src={"./stress_score/stress_score_2024-04-03.png"} alt="stress_"/>
      </div>
    );
  };
  
  export default TestPage;