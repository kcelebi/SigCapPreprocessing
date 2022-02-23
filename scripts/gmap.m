function gmap(data)
    files = dir(data);
    files = files(3:end);

    files = arrayfun(@(x) [data '/' x.name], files, "UniformOutput", false);
    parse_data = arrayfun(@(x) parse(x{1}), files, "UniformOutput", false);
    parse_data = [parse_data{1:end}]';
    
    g_plot(parse_data);
end

function out = parse(x)

    fid = fopen(x);
    raw = fread(fid, inf);
    str = char(raw');
    fclose(fid);
    
    val = jsondecode(str);
    
    ss = -300;
    lat = val.location.latitude;
    lon = val.location.longitude;
    
    if ~isempty(val.cell_info)
        ss = val.cell_info.ss;
    end
    
    out = [ss; lat; lon];
end

function g_plot(x)
    lat = x(:, 2)';
    lon = x(:, 3)';
%     ss = x(:, 1);

    plot(lon, lat, '.','MarkerSize', 20)
    plot_google_map('maptype', 'hybrid', 'language', 'fr', 'showLabels', 1)
    
end
