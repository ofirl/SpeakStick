import { UseCreateMutationWrapperOptions, UseCreateQueryWrapperOptionsShort, axiosClient, useCreateMutation, useCreateQuery } from "./helpers";

export const useRestartStickController = (options?: UseCreateMutationWrapperOptions<boolean, void>) => {
  return useCreateMutation(
    {
      mutationFn: () =>
        axiosClient.get("/restart/stick-controller").then(value => value.status === 200),
      successMsg: "Stick controller restarted",
      errorMsg: "Error restarting stick controller",
      ...options
    }
  )
};

export const useResetToFactorySettings = (options?: UseCreateMutationWrapperOptions<boolean, void>) => {
  return useCreateMutation(
    {
      mutationFn: () => axiosClient.get("/reset_factory_settings").then(value => value.status === 200),
      successMsg: "Application is resetting to factory settings, this might take a few seconds",
      errorMsg: "Error resetting application to factory settings",
      ...options
    }
  )
};

export type BatteryPercentResult = { percent: number, isCharging: boolean };
export const useGetBatteryPercent = (options?: UseCreateQueryWrapperOptionsShort<BatteryPercentResult>) => {
  return useCreateQuery({
    queryKey: ['battery', 'percent'],
    queryFn: () => axiosClient.get("/battery/percent").then(value => value.data as BatteryPercentResult),
    refetchInterval: 30000,
    errorMsg: "Error getting battery percentage",
    ...options
  })
};

export const servicesOptions = ["speakstick", "speakstick-management-server", "nginx"] as const;
export type Services = typeof servicesOptions[number];
export const useGetServiceLogs = (service: Services, options?: UseCreateQueryWrapperOptionsShort<string>) => {
  return useCreateQuery(
    {
      queryKey: ['logs', service],
      queryFn: () => axiosClient.get(`/logs/${service}`).then(value => value.data as string),
      refetchInterval: 10000,
      errorMsg: "Error getting service logs",
      ...options
    },
  )
};