module TC_Hdd (clk, rst, seek, load, save, in, out);
    parameter BIT_DEPTH = 256;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [63:0] seek;
    input load;
    input save;
    input [63:0] in;
    output [63:0] out;
    
    reg [63:0] mem [0:BIT_DEPTH-1];
    reg [63:0] mp;
    
    initial begin
        hexfile = HEX_FILE;
        i = ($value$plusargs(ARG_SIG, hexfile));
        $display("loading %0s", hexfile);
        fd = $fopen(hexfile, "r");
        if (fd) begin
            i = 0;
            while (i < BIT_DEPTH && !$feof(fd)) begin
                mem[i][7:0] = $fgetc(fd);
                if (!$feof(fd)) begin
                    mem[i][15:8] = $fgetc(fd);
                    if (!$feof(fd)) begin
                        mem[i][23:16] = $fgetc(fd);
                        if (!$feof(fd)) begin
                            mem[i][31:24] = $fgetc(fd);
                            if (!$feof(fd)) begin
                                mem[i][39:32] = $fgetc(fd);
                                if (!$feof(fd)) begin
                                    mem[i][47:40] = $fgetc(fd);
                                    if (!$feof(fd)) begin
                                        mem[i][55:48] = $fgetc(fd);
                                        if (!$feof(fd)) begin
                                            mem[i][63:56] = $fgetc(fd);
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
                i = i + 1;
            end
            $display("read %d bytes", i);
        end else begin
            $display("file not found");
        end
        $fclose(fd);
        out = {64{1'b0}};
    end

    always @ (posedge clk) begin
        if (rst) begin
            mp = {64{1'b0}};
            out = {64{1'b0}};
        end else begin
            mp <= mp + seek;
            if (load) begin
                out <= mem[mp];
            end
        end
    end
    
    always @ (negedge clk) begin
        if (save && !rst) begin
            mem[mp] <= in;
        end
    end
endmodule
