import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a PDF resume.')
      return
    }

    if (!jobDescription.trim()) {
      setError('Please enter a job description.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      // Step 1: Upload resume
      const formData = new FormData()
      formData.append('file', file)

      const uploadResponse = await fetch(
        'http://127.0.0.1:8000/api/resume/upload',
        {
          method: 'POST',
          body: formData,
        }
      )

      if (!uploadResponse.ok) {
        throw new Error('Resume upload failed.')
      }

      const uploadData = await uploadResponse.json()

      // Step 2: Analyze resume with job description
      const analyzeResponse = await fetch(
        'http://127.0.0.1:8000/api/resume/analyze',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            resume_text: uploadData.text,
            job_description: jobDescription,
          }),
        }
      )

      if (!analyzeResponse.ok) {
        const errorData = await analyzeResponse.json()
        throw new Error(
          errorData.detail || 'Resume analysis failed.'
        )
      }

      const analysisData = await analyzeResponse.json()

      setResult(analysisData)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">

        <h1>AI Resume Analyzer</h1>

        <p className="subtitle">
          Analyze your resume against a job description using AI
        </p>

        <div className="card">

          <label>Upload Resume</label>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {
              setFile(e.target.files[0])
              setError('')
            }}
          />

          {file && (
            <p className="file-name">
              Selected: {file.name}
            </p>
          )}

          <label>Job Description</label>

          <textarea
            rows="8"
            placeholder="Paste the job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          <button
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>

          {error && (
            <div className="error">
              {error}
            </div>
          )}
        </div>

        {result && (
          <div className="results">

            <h2>Resume Analysis</h2>

            <div className="score-card">
              <h3>Match Score</h3>
              <div className="score">
                {result.match_score}%
              </div>
            </div>

            <div className="result-card">
              <h3>Candidate Information</h3>

              <p>
                <strong>Name:</strong>{' '}
                {result.candidate_information?.name || 'Not provided'}
              </p>

              <p>
                <strong>Email:</strong>{' '}
                {result.candidate_information?.email || 'Not provided'}
              </p>

              <p>
                <strong>Phone:</strong>{' '}
                {result.candidate_information?.phone || 'Not provided'}
              </p>

              <p>
                <strong>Location:</strong>{' '}
                {result.candidate_information?.location || 'Not provided'}
              </p>
            </div>

            <div className="result-card">
              <h3>Matching Skills</h3>

              {result.matching_skills?.length > 0 ? (
                <ul>
                  {result.matching_skills.map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))}
                </ul>
              ) : (
                <p>No matching skills found.</p>
              )}
            </div>

            <div className="result-card">
              <h3>Missing Skills</h3>

              {result.missing_skills?.length > 0 ? (
                <ul>
                  {result.missing_skills.map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))}
                </ul>
              ) : (
                <p>No missing skills found.</p>
              )}
            </div>

            <div className="result-card">
              <h3>Improvement Suggestions</h3>

              {result.improvement_suggestions?.length > 0 ? (
                <ul>
                  {result.improvement_suggestions.map(
                    (suggestion, index) => (
                      <li key={index}>{suggestion}</li>
                    )
                  )}
                </ul>
              ) : (
                <p>No suggestions available.</p>
              )}
            </div>

          </div>
        )}
      </div>
    </div>
  )
}

export default App