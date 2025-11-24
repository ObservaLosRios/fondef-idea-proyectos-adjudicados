import pandas as pd
import plotly.express as px
import os

try:
    # Load data
    df_2000 = pd.read_csv('data/processed/fondef_2000_2011_processed.csv')
    df_2012 = pd.read_csv('data/processed/fondef_2012_2017_processed.csv')

    # Process
    df_all = pd.concat([df_2000, df_2012], ignore_index=True)
    df_all = df_all[df_all['year'] > 1990]

    # Plot
    projects_per_year = df_all.groupby('year').size().reset_index(name='Cantidad')

    fig2 = px.line(projects_per_year, 
                   x='year', 
                   y='Cantidad', 
                   title='Evolución de la Cantidad de Proyectos por Año',
                   markers=True,
                   labels={'year': 'Año', 'Cantidad': 'N° de Proyectos'})

    fig2.update_traces(line_color='#E63946', line_width=3)
    fig2.update_layout(xaxis_tickmode='linear')

    # Save
    os.makedirs('docs', exist_ok=True)
    output_path = 'docs/evolucion_proyectos_anio.html'
    fig2.write_html(output_path)
    print(f"HTML file created successfully at {output_path}")
except Exception as e:
    print(f"Error: {e}")
