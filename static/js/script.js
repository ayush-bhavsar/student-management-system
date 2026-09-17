document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert').forEach((alert) => {
    window.setTimeout(() => {
      if (window.bootstrap) bootstrap.Alert.getOrCreateInstance(alert).close();
    }, 4000);
  });
});
