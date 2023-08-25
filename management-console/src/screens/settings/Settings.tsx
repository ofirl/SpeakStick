import { useGetConfigs } from "../../api/configs";


export const Settings = () => {
    const { data: configs } = useGetConfigs();
    console.log(configs)

    return <div>
        settings
    </div>
};