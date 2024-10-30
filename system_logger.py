class SystemLogger:
    log_count = 0

    @staticmethod
    def log_error(message):
        SystemLogger.log_count += 1
        print(f"ERROR: {message}")

    @staticmethod
    def log_info(message):
        SystemLogger.log_count += 1
        print(f"INFO: {message}")

    @staticmethod
    def get_log_count():
        return SystemLogger.log_count
