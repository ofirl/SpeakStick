import { useVersionsChangeLog } from "../../api/versions"

export const ChangeLog = () => {
    const { data: changeLog = [] } = useVersionsChangeLog();

    return (
        <div style={{ maxWidth: "70rem", gap: "1rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
            Change Log
            {
                changeLog.map(c => (
                    <div>
                        {c.title}
                        {c.description}
                    </div>
                ))
            }
        </div>
    )
}