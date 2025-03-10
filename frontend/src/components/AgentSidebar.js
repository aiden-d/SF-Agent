import React from "react";
import {
  Box,
  Button,
  Typography,
  Paper,
  Divider,
  Stack,
  Alert,
} from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import StopIcon from "@mui/icons-material/Stop";

function AgentSidebar({ status, onStart, onStop, linkedInCredentialsSet }) {
  const isRunning = status.status !== "stopped";

  // Format status text
  const formatStatus = (status) => {
    if (!status) return "Unknown";
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  // Get status class
  const getStatusClass = (status) => {
    if (status === "running" || status === "searching for jobs") {
      return "status-running";
    } else if (status === "stopped") {
      return "status-stopped";
    } else {
      return "status-waiting";
    }
  };

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <Paper className="agent-sidebar">
      <Typography variant="h6" gutterBottom>
        Agent Control Panel
      </Typography>
      <Divider sx={{ mb: 2 }} />

      {!linkedInCredentialsSet && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          Please set your LinkedIn credentials above to enable the agent.
        </Alert>
      )}

      <Box sx={{ mb: 3 }}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Current Status
        </Typography>
        <div className={`agent-status ${getStatusClass(status.status)}`}>
          {formatStatus(status.status)}
        </div>
      </Box>

      <Stack spacing={2} sx={{ mb: 3 }}>
        <Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Jobs Found
          </Typography>
          <Typography variant="h5">{status.job_count || 0}</Typography>
        </Box>

        <Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Total Jobs Searched
          </Typography>
          <Typography variant="h5">
            {status.total_jobs_searched || 0}
          </Typography>
        </Box>

        {status.start_time && (
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Started At
            </Typography>
            <Typography variant="body1">
              {formatDate(status.start_time)}
            </Typography>
          </Box>
        )}

        {status.running_time && (
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Running Time
            </Typography>
            <Typography variant="body1">{status.running_time}</Typography>
          </Box>
        )}
      </Stack>

      <Stack direction="row" spacing={2}>
        <Button
          variant="contained"
          className="start-button"
          startIcon={<PlayArrowIcon />}
          onClick={onStart}
          disabled={isRunning || !linkedInCredentialsSet}
          fullWidth
        >
          Start Agent
        </Button>

        <Button
          variant="contained"
          className="stop-button"
          startIcon={<StopIcon />}
          onClick={onStop}
          disabled={!isRunning}
          fullWidth
        >
          Stop Agent
        </Button>
      </Stack>
    </Paper>
  );
}

export default AgentSidebar;
