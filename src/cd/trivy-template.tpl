{{- $critical := 0 }}{{- $high := 0 }}{{- $med := 0 }}{{- $low := 0 }}{{- $unknown := 0 }}
{{- range . }}{{- range .Vulnerabilities }}
{{- if  eq .Severity "CRITICAL" }}
  {{- $critical = add $critical 1 }}
{{- end }}
{{- if  eq .Severity "HIGH" }}
  {{- $high = add $high 1 }}
{{- end }}
{{- if  eq .Severity "MEDIUM" }}
  {{- $med = add $med 1 }}
{{- end }}
{{- if  eq .Severity "LOW" }}
  {{- $low = add $low 1 }}
{{- end }}
{{- if  eq .Severity "UNKNOWN" }}
  {{- $unknown = add $unknown 1 }}
{{- end }}
{{- end }}
{{- end }}
Critical: {{ $critical }} High: {{ $high }} Medium: {{ $med }} Low: {{ $low }} Unknown: {{ $unknown }}
