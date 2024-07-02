function convert_s2p_to_s1p(s2p_filename, s1p_filename)
    % Check if the input file exists
    if ~isfile(s2p_filename)
        error('The specified S2P file does not exist.');
    end

    % Open the S2P file for reading
    fid = fopen(s2p_filename, 'r');
    if fid == -1
        error('Failed to open the S2P file.');
    end

    % Read the header of the S2P file
    header = {};
    while true
        line = fgetl(fid);
        if ~ischar(line)
            error('Unexpected end of file.');
        end
        header{end+1} = line; %#ok<*AGROW>
        if startsWith(line, '#')
            break;
        end
    end

    % Determine the format and frequency unit
    header_line = header{end};
    tokens = strsplit(header_line);
    if length(tokens) < 6
        error('Invalid S2P header format.');
    end
    freq_unit = tokens{2};
    data_format = tokens{6};

    % Read the S-parameter data
    data = [];
    while true
        line = fgetl(fid);
        if ~ischar(line)
            break;
        end
        if isempty(line) || startsWith(line, '!')
            continue;
        end
        values = str2double(strsplit(line));
        values = values(2:end-1);
        if length(values) ~= 9
            error('Invalid S2P data format.');
        end
        data(end+1, :) = values; %#ok<*AGROW>
    end

    % Close the S2P file
    fclose(fid);
    
    % Extract S-Parameter from data
    freq = data(:, 1);
    s11 = data(:, 2:3);

    % Open the S1P file for writing
    fid = fopen(s1p_filename, 'w');
    if fid == -1
        error('Failed to open the S1P file for writing.');
    end

    % Write the header to the S1P file
    for i = 1:length(header)-1
        fprintf(fid, '%s\n', header{i});
    end
    fprintf(fid, '# %s S DB R 50\n', freq_unit); % Assuming S1P format with Real/Imaginary format

    % Write the S11 data to the S1P file
    for i = 1:length(freq)
        fprintf(fid, '%e %e %e\n', freq(i), s11(i, 1), s11(i, 2));
    end

    % Close the S1P file
    fclose(fid);

    fprintf('Conversion completed: %s -> %s\n', s2p_filename, s1p_filename);
end
