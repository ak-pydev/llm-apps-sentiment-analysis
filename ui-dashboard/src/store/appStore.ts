interface AppState {
  selectedApp: string | null;
  loading: boolean;
}

const initialState: AppState = {
  selectedApp: null,
  loading: false,
};

export const appStore = {
  state: initialState,

  setSelectedApp(appName: string) {
    this.state.selectedApp = appName;
  },

  getSelectedApp() {
    return this.state.selectedApp;
  },

  setLoading(loading: boolean) {
    this.state.loading = loading;
  },

  isLoading() {
    return this.state.loading;
  },

  reset() {
    this.state = initialState;
  },
};
