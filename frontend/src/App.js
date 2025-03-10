import React, { useState, useEffect } from "react";
import { Box, Container, Grid, Typography } from "@mui/material";
import JobTable from "./components/JobTable";
import AgentSidebar from "./components/AgentSidebar";
import LinkedInLogin from "./components/LinkedInLogin";
import axios from "axios";

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [linkedInCredentialsSet, setLinkedInCredentialsSet] = useState(false);
  const [agentStatus, setAgentStatus] = useState({
    status: "stopped",
    job_count: 0,
    total_jobs_searched: 0,
    running_time: null,
    start_time: null,
  });
  const [refreshInterval, setRefreshInterval] = useState(null);

  // Check if LinkedIn credentials are set
  const checkLinkedInCredentials = async () => {
    try {
      const response = await axios.get("/api/linkedin/credentials/status");
      setLinkedInCredentialsSet(response.data.set);
    } catch (error) {
      console.error("Error checking LinkedIn credentials:", error);
      setLinkedInCredentialsSet(false);
    }
  };

  // Fetch jobs
  const fetchJobs = async () => {
    try {
      const response = await axios.get("/jobs");
      setJobs(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching jobs:", error);
      setLoading(false);
    }
  };

  // Fetch agent status
  const fetchAgentStatus = async () => {
    try {
      const response = await axios.get("/agent/status");
      setAgentStatus(response.data);
    } catch (error) {
      console.error("Error fetching agent status:", error);
    }
  };

  // Start the agent
  const startAgent = async () => {
    if (!linkedInCredentialsSet) {
      alert("Please set LinkedIn credentials before starting the agent.");
      return;
    }

    try {
      await axios.post("/agent/start");
      fetchAgentStatus();
      // Start refreshing jobs and status regularly
      if (!refreshInterval) {
        const interval = setInterval(() => {
          fetchJobs();
          fetchAgentStatus();
        }, 5000); // Every 5 seconds
        setRefreshInterval(interval);
      }
    } catch (error) {
      console.error("Error starting agent:", error);
    }
  };

  // Stop the agent
  const stopAgent = async () => {
    try {
      await axios.post("/agent/stop");
      fetchAgentStatus();
      // Clear the refresh interval
      if (refreshInterval) {
        clearInterval(refreshInterval);
        setRefreshInterval(null);
      }
    } catch (error) {
      console.error("Error stopping agent:", error);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchJobs();
    fetchAgentStatus();
    checkLinkedInCredentials();

    // Clear interval on unmount
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, []);

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        SF Software Engineering Jobs with Visa Sponsorship
      </Typography>
      <Typography variant="body1" gutterBottom>
        Automatically finding software engineering roles in San Francisco that
        offer visa sponsorship.
      </Typography>

      <Box sx={{ mt: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <LinkedInLogin
              onCredentialsSet={(status) => {
                setLinkedInCredentialsSet(status);
                // Refresh agent status and jobs after setting credentials
                fetchAgentStatus();
                fetchJobs();
              }}
            />
          </Grid>
          <Grid item xs={12} md={9}>
            <JobTable jobs={jobs} loading={loading} />
          </Grid>
          <Grid item xs={12} md={3}>
            <AgentSidebar
              status={agentStatus}
              onStart={startAgent}
              onStop={stopAgent}
              linkedInCredentialsSet={linkedInCredentialsSet}
            />
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}

export default App;
