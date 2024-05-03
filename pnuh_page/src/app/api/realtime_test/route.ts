// import { NextResponse } from 'next/server';
// import { exec } from 'child_process';
// import path from 'path';

// export async function POST(request: Request) {
//   const { date } = await request.json();

//   const pythonScriptPath = path.join(process.cwd(), '..', '..', '..', '..', 'hrv_proc', 'hrv.py');
//   const pythonScriptDir = path.dirname(pythonScriptPath);
//   exec('안녕?')
//   exec(`cd ${pythonScriptDir} && python stress_score.py ${date}`, (error, stdout, stderr) => {
//     if (error) {
//       console.error(`Error: ${error.message}`);
//       return NextResponse.json({ error: 'Failed to run Python script' }, { status: 500 });
//     }

//     const { stressScore, plotData } = JSON.parse(stdout);
//     return NextResponse.json({ stressScore, plotData });
//   });
// }

import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(request: Request) {
  const { date } = await request.json();

  try {
    const { stdout, stderr } = await execAsync('dir');

    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return NextResponse.json({ error: 'Command execution error' }, { status: 500 });
    }

    console.log(`stdout: ${stdout}`);
    return NextResponse.json({ message: 'Command executed successfully', output: stdout });
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}